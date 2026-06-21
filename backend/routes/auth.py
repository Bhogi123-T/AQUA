from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import time
from core.auth_utils import get_trans, get_role
from core.db import USERS_DB, save_json, USERS_FILE, APP_CONFIG
from core.knowledge_base import GLOBAL_AQUA_REGIONS
from core.supabase_client import supabase, is_mock
from core.oauth_client import google

# Temporary store for OTPs
OTP_STORE = {}
auth_bp = Blueprint('auth', __name__)

LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 900

def check_rate_limit(ip):
    now = time.time()
    entry = LOGIN_ATTEMPTS.get(ip, {})
    locked_until = entry.get("locked_until", 0)
    if locked_until and now < locked_until:
        return False, int(locked_until - now)
    return True, 0

def record_failed_attempt(ip):
    now = time.time()
    entry = dict(LOGIN_ATTEMPTS.get(ip, {"count": 0, "locked_until": 0}))
    entry["count"] = entry.get("count", 0) + 1
    if entry["count"] >= MAX_LOGIN_ATTEMPTS:
        entry["locked_until"] = now + LOCKOUT_SECONDS
        entry["count"] = 0
    LOGIN_ATTEMPTS[ip] = entry

def clear_failed_attempts(ip):
    LOGIN_ATTEMPTS.pop(ip, None)

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or request.form
    ip = request.remote_addr
    trans, lang = get_trans()
    
    allowed, wait_sec = check_rate_limit(ip)
    if not allowed:
        mins = wait_sec // 60
        secs = wait_sec % 60
        return jsonify({
            "status": "error",
            "message": f"Too many failed attempts. Account locked for {mins}m {secs}s. Please try again later."
        }), 429
    
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    AUTH_ERROR = "Invalid credentials. Please check your email and password."
    is_valid = False
    
    if not is_mock:
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            is_valid = True
            # Ensure user exists in local DB for role fetching
            if email not in USERS_DB:
                meta = res.user.user_metadata if hasattr(res, 'user') and res.user else {}
                USERS_DB[email] = {
                    "name": meta.get("name", "User"),
                    "role": meta.get("role", "farmer"),
                    "password": "",
                    "joined_at": datetime.now().isoformat(),
                    "auth_method": "supabase"
                }
                save_json(USERS_FILE, USERS_DB)
        except Exception as e:
            AUTH_ERROR = str(e)
    else:
        if email in USERS_DB:
            hashed_pw = USERS_DB[email].get("password", "")
            if hashed_pw:
                if ":" in hashed_pw: is_valid = check_password_hash(hashed_pw, password)
                else: is_valid = (hashed_pw == password)
        
    if is_valid:
        user_data = USERS_DB.get(email, {})
        clear_failed_attempts(ip)
        session.clear()
        session["user"] = email
        session["user_name"] = user_data.get("name", "User")
        session["user_pic"] = user_data.get("picture", "")
        session["role"] = user_data.get("role", "farmer")
        session.permanent = True
        
        return jsonify({
            "status": "success",
            "user": {
                "email": email,
                "name": session["user_name"],
                "role": session["role"],
                "pic": session["user_pic"]
            }
        })
    else:
        record_failed_attempt(ip)
        attempts_left = MAX_LOGIN_ATTEMPTS - LOGIN_ATTEMPTS.get(ip, {}).get("count", 0)
        return jsonify({
            "status": "error",
            "message": AUTH_ERROR,
            "attempts_remaining": max(0, attempts_left)
        }), 401

@auth_bp.route("/api/request-otp", methods=["POST"])
def api_request_otp():
    data = request.get_json(silent=True) or request.form
    phone = data.get("phone", "").strip()
    
    if not phone:
        return jsonify({"status": "error", "message": "Phone number is required"}), 400
        
    # Generate a random 6 digit OTP
    otp = str(random.randint(100000, 999999))
    OTP_STORE[phone] = {"otp": otp, "expires_at": time.time() + 300} # 5 minutes expiry
    
    # In a real app, integrate Twilio here to send SMS
    print(f"[OTP DEV MODE] Sent OTP {otp} to {phone}")
    
    return jsonify({
        "status": "success",
        "message": "OTP sent successfully"
    })

@auth_bp.route("/api/verify-otp", methods=["POST"])
def api_verify_otp():
    data = request.get_json(silent=True) or request.form
    phone = data.get("phone", "").strip()
    otp = data.get("otp", "").strip()
    
    record = OTP_STORE.get(phone)
    if not record or record["expires_at"] < time.time():
        return jsonify({"status": "error", "message": "OTP expired or not requested"}), 400
        
    if record["otp"] != otp and otp != "123456": # 123456 is a master OTP for testing
        return jsonify({"status": "error", "message": "Invalid OTP"}), 400
        
    # OTP is valid, log the user in or register
    email = f"{phone}@otp.aqua"
    if email not in USERS_DB:
        USERS_DB[email] = {
            "name": f"Farmer {phone[-4:]}",
            "role": "farmer",
            "joined_at": datetime.now().isoformat(),
            "auth_method": "otp",
            "phone": phone
        }
        save_json(USERS_FILE, USERS_DB)
        
    session.clear()
    session["user"] = email
    session["user_name"] = USERS_DB[email]["name"]
    session["role"] = USERS_DB[email]["role"]
    session.permanent = True
    
    return jsonify({
        "status": "success",
        "user": {
            "email": email,
            "name": session["user_name"],
            "role": session["role"]
        }
    })

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    trans, lang = get_trans()
    if 'user' in session:
        role = session.get('role', 'farmer')
        if role == 'admin': return redirect(url_for('main.admin_dashboard'))
        if role == 'farmer': return redirect(url_for('farmer.farmer_hub'))
        if role == 'hatchery': return redirect(url_for('hatchery.hatchery_dashboard'))
        if role == 'lab_tech': return redirect(url_for('lab_tech.lab_tech_dashboard'))
        if role == 'buyer' or role == 'exporter': return redirect(url_for('buyer.buyer_dashboard_route'))
        return redirect(url_for('main.dashboard'))
    
    if request.method == "POST":
        res = api_login()
        if res.status_code == 200:
            data = res.get_json()
            flash(f"Welcome back, {data['user']['name']}!", "success")
            role = data['user']['role']
            if role == "admin": return redirect(url_for("main.admin_dashboard"))
            if role == "farmer": return redirect(url_for("farmer.farmer_hub"))
            if role == "hatchery": return redirect(url_for("hatchery.hatchery_dashboard"))
            if role == "lab_tech": return redirect(url_for("lab_tech.lab_tech_dashboard"))
            if role == "buyer": return redirect(url_for("buyer.buyer_dashboard_route"))
            return redirect(url_for("main.dashboard"))
        else:
            return render_template("login.html", trans=trans, lang=lang, error=res.get_json().get('message'))
            
    return render_template("login.html", trans=trans, lang=lang)

@auth_bp.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json(silent=True) or request.form
    trans, lang = get_trans()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "farmer")
    
    if email in USERS_DB:
        return jsonify({"status": "error", "message": "Email already registered."}), 400
    
    if not is_mock:
        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        "role": role
                    }
                }
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    USERS_DB[email] = {
        "name": name,
        "password": generate_password_hash(password) if is_mock else "",
        "role": role,
        "joined_at": datetime.now().isoformat(),
        "auth_method": "supabase" if not is_mock else "local"
    }
    
    if email == "bhogeswararaothirumalasetti@gmail.com":
        USERS_DB[email]["role"] = "admin"
        
    save_json(USERS_FILE, USERS_DB)
    
    session["user"] = email
    session["user_name"] = name
    session["role"] = USERS_DB[email]["role"]
    
    return jsonify({
        "status": "success",
        "user": {
            "email": email,
            "name": name,
            "role": session["role"]
        }
    })

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    trans, lang = get_trans()
    if request.method == "POST":
        res = api_signup()
        if res.status_code == 200:
            data = res.get_json()
            flash(f"Account created as {data['user']['role'].title()}! Welcome.", "success")
            role = data['user']['role']
            if role == "admin": return redirect(url_for("main.admin_dashboard"))
            if role == "farmer": return redirect(url_for("farmer.farmer_hub"))
            return redirect(url_for("main.dashboard"))
        else:
            flash(res.get_json().get('message'), "error")
            return redirect(url_for("auth.signup", lang=lang))
                
    return render_template("signup.html", trans=trans, lang=lang)

@auth_bp.route("/api/logout")
def api_logout():
    session.pop("user", None)
    session.pop("user_name", None)
    session.pop("role", None)
    session.pop("user_pic", None)
    return jsonify({"status": "success", "message": "Logged out"})

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.landing"))

@auth_bp.route("/login/mock-google")
def mock_google_callback():
    user_info = {
        "email": "local-tester@aqua-ecosystem.io",
        "name": "Local Test User (Demo)",
    }
    email = user_info.get('email')
    name = user_info.get('name')
    
    if email not in USERS_DB:
        session["temp_user"] = {
            "name": name,
            "email": email,
            "auth_method": "dev_mock"
        }
        return redirect(url_for("auth.register_role"))
    
    session["user"] = email
    session["user_name"] = name
    session["role"] = USERS_DB[email]["role"]
    
    _, lang = get_trans()
    flash(f"Success! Logged in as {name} ({session['role']}). This is a local TEST session.", "success")
    
    role = session["role"]
    if role == "admin": return redirect(url_for("main.admin_dashboard"))
    if role == "farmer": return redirect(url_for("farmer.farmer_hub"))
    return redirect(url_for("main.dashboard"))

@auth_bp.route('/login/google')
def google_login():
    if not os.getenv('GOOGLE_CLIENT_ID'):
        return redirect(url_for('auth.mock_google_callback'))
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        # The id_token contains the user info already parsed by authlib!
        user_info = token.get('userinfo')
        if not user_info:
            # Fallback if id_token was missing
            user_info = google.parse_id_token(token, nonce=None)
    except Exception as e:
        print(f"\n[!!!] GOOGLE CALLBACK ERROR: {str(e)}\n")
        flash(f"Google login failed: {str(e)}", "error")
        return redirect(url_for("auth.login"))

    email = user_info.get('email')
    name = user_info.get('name')
    picture = user_info.get('picture')
    
    if email not in USERS_DB:
        session["temp_user"] = {
            "name": name,
            "email": email,
            "picture": picture,
            "auth_method": "google"
        }
        return redirect(url_for("auth.register_role"))
        
    session["user"] = email
    session["user_name"] = name
    session["role"] = USERS_DB[email].get("role", "farmer")
    session["user_pic"] = USERS_DB[email].get("picture", picture)
    session.permanent = True
    
    flash(f"Welcome back, {name}!", "success")
    role = session["role"]
    if role == "admin": return redirect(url_for("main.admin_dashboard"))
    if role == "farmer": return redirect(url_for("farmer.farmer_hub"))
    if role == "hatchery": return redirect(url_for("hatchery.hatchery_dashboard"))
    if role == "lab_tech": return redirect(url_for("lab_tech.lab_tech_dashboard"))
    if role == "buyer": return redirect(url_for("buyer.buyer_dashboard_route"))
    return redirect(url_for("main.dashboard"))

@auth_bp.route("/register-role", methods=["GET", "POST"])
def register_role():
    trans, lang = get_trans()
    temp_user = session.get("temp_user")
    
    if 'user' in session:
        return redirect(url_for('main.home_page'))
    if not temp_user:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        role = request.form.get("role", "farmer")
        country = request.form.get("country", "")
        state = request.form.get("state", "")
        district = request.form.get("district", "")
        email = temp_user["email"]
        
        USERS_DB[email] = {
            "name": temp_user.get("name", "User"),
            "role": role,
            "location": {
                "country": country,
                "state": state,
                "district": district
            },
            "picture": temp_user.get("picture", ""),
            "joined_at": datetime.now().isoformat(),
            "auth_method": temp_user.get("auth_method", "google")
        }
        save_json(USERS_FILE, USERS_DB)
        
        session.clear()
        session["user"] = email
        session["user_name"] = USERS_DB[email]["name"]
        session["user_pic"] = USERS_DB[email].get("picture", "")
        session["role"] = role
        session["user_location"] = USERS_DB[email]["location"]
        session.permanent = True
        
        flash(f"Welcome to AquaSphere, {session['user_name']}! Your {role.title()} portal is ready.", "success")
        
        if role == "admin": return redirect(url_for("main.admin_dashboard"))
        return redirect(url_for("main.dashboard"))
        
    return render_template("register_role.html", trans=trans, lang=lang, geography=GLOBAL_AQUA_REGIONS)
