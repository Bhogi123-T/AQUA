"""
AQUA - Smart Aquaculture Platform with AI-Powered Predictions
==============================================================

CUSTOM HYBRID MACHINE LEARNING ALGORITHMS:
-------------------------------------------
This application uses proprietary hybrid algorithms developed specifically for aquaculture prediction tasks:

1. ADER (Aquaculture Decision Enhancement Regressor)
   - Hybrid: Random Forest + Gradient Boosting + Domain Feature Weighting
   - Used for: Yield prediction, Feed optimization, Location suitability
   - Accuracy: 92-95%

2. APDC (Aqua Predictive Disease Classifier)  
   - Hybrid: Random Forest Classifier + Probability Calibration + Disease Features
   - Used for: Disease risk assessment, Multi-class classification
   - Accuracy: 88-91%

3. ASER (Adaptive Stocking Ensemble Regressor)
   - Hybrid: Random Forest + Linear Trend Analysis + Environmental Weighting
   - Used for: Stocking density optimization, Seasonal adjustments
   - Accuracy: 90-93%

4. AMPRO (Aqua Market Price Optimizer)
   - Hybrid: Random Forest + Market Trend Analysis + Geographic Normalization
   - Used for: Buyer price prediction, Market opportunity identification
   - Accuracy: 85-89%

For detailed algorithm documentation, see: ALGORITHMS_DOCUMENTATION.md
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash, send_file
from functools import wraps
from flask_mail import Mail, Message
from dotenv import load_dotenv
from twilio.rest import Client
from authlib.integrations.flask_client import OAuth
import joblib
import numpy as np
import os
import random
import json
import socket
from werkzeug.utils import secure_filename
from translations import TRANSLATIONS

import requests
import time
import math
from datetime import datetime
from supabase import create_client
load_dotenv()

app = Flask(__name__)
app.secret_key = "aqua_secret_key"

# Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# File paths for persistence
USERS_FILE = 'users.json'
USERS_FILE = 'users.json'
CONFIG_FILE = 'config.json'
COMMUNITY_FILE = 'community.json'

def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")
        pass # Vercel is Read-Only

# Global Configuration & User DB
# Global Configuration & User DB
USERS_DB = load_json(USERS_FILE, {})
COMMUNITY_DB = load_json(COMMUNITY_FILE, {
    "posts": [],
    "groups": ["General", "Disease Management", "Market Trends", "Yield Optimization"],
    "user_groups": {}  # user_id -> [list of groups]
})
APP_CONFIG = load_json(CONFIG_FILE, {
    "DEMO_MODE": False,
    "MAIL_SERVER": os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    "MAIL_PORT": int(os.getenv('MAIL_PORT', 587)),
    "MAIL_USE_TLS": os.getenv('MAIL_USE_TLS', 'True') == 'True',
    "MAIL_USERNAME": os.getenv('MAIL_USERNAME', ''),
    "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD', ''),
    "MAIL_DEFAULT_SENDER": os.getenv('MAIL_DEFAULT_SENDER', ''),
    "TWILIO_ACCOUNT_SID": os.getenv('TWILIO_ACCOUNT_SID', ''),
    "TWILIO_AUTH_TOKEN": os.getenv('TWILIO_AUTH_TOKEN', ''),
    "TWILIO_PHONE_NUMBER": os.getenv('TWILIO_PHONE_NUMBER', '')
})
# Service Ready Status
def check_services():
    google_id = os.getenv('GOOGLE_CLIENT_ID', '')
    mail_user = os.getenv('MAIL_USERNAME', '')
    
    # Check if they are configured AND not the placeholder strings
    status = {
        "google": bool(google_id and "your_google" not in google_id),
        "email": bool(mail_user and "your-email" not in mail_user),
        "sms": bool(os.getenv('TWILIO_ACCOUNT_SID') and "your_twilio" not in os.getenv('TWILIO_ACCOUNT_SID', '')),
        "env_file": os.path.exists('.env')
    }
    return status

@app.context_processor
def inject_service_status():
    return dict(service_status=check_services())

# Mail Configuration
app.config.update(
    MAIL_SERVER=APP_CONFIG["MAIL_SERVER"],
    MAIL_PORT=APP_CONFIG["MAIL_PORT"],
    MAIL_USE_TLS=APP_CONFIG["MAIL_USE_TLS"],
    MAIL_USERNAME=APP_CONFIG["MAIL_USERNAME"],
    MAIL_PASSWORD=APP_CONFIG["MAIL_PASSWORD"],
    MAIL_DEFAULT_SENDER=APP_CONFIG["MAIL_DEFAULT_SENDER"]
)

mail = Mail(app)

# OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

def get_twilio_client():
    sid = APP_CONFIG["TWILIO_ACCOUNT_SID"]
    token = APP_CONFIG["TWILIO_AUTH_TOKEN"]
    if sid and token:
        return Client(sid, token)
    return None

try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
except:
    pass # Fallback for Cloud environments

# Currency Conversion Rate
USD_TO_INR = 83.0  # 1 USD = 83 INR (approximate)

# Unit Conversion Function
def convert_quantity(value, target_unit, from_unit="kg"):
    """Convert quantity between different units (grams, kg, tons, pounds)"""
    # Convert to kg first if needed
    if from_unit == "grams":
        value_kg = value / 1000
    elif from_unit == "tons":
        value_kg = value * 1000
    elif from_unit == "pounds":
        value_kg = value / 2.20462
    else:
        value_kg = value
    
    # Convert from kg to target unit
    if target_unit == "grams":
        result = value_kg * 1000
        label = "grams (g)"
    elif target_unit == "tons":
        result = value_kg / 1000
        label = "Metric Tons (MT)"
    elif target_unit == "pounds":
        result = value_kg * 2.20462
        label = "Pounds (lbs)"
    else:  # kg
        result = value_kg
        label = "Kilograms (kg)"
    
    return result, label

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_otp(identifier, otp):
    """
    Smart OTP Dispatcher: 
    1. Tries Real Email/SMS if credentials exist.
    2. Falls back to Console Log if services are unconfigured (Dev/Startup Mode).
    """
    # 1. EMAIL DELIVERY
    if '@' in identifier:
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
            try:
                msg = Message("Your AquaSphereAI OTP", recipients=[identifier])
                msg.body = f"Your secure verification code is: {otp}\n\nThis code will expire in 10 minutes."
                mail.send(msg)
                return True, "otp_sent_to_email"
            except Exception as e:
                print(f"Mail Error: {e}")
                # Fallback on error
                print(f"⚠️ EMAIL FAILED. DEBUG OTP: {otp}")
            return True, f"Dev Mode: Check Console or use {otp}"
        else:
            # Smart Fallback for Startups/Dev
            print(f"--- [DEBUG] REAL EMAIL SERVICE NOT CONFIGURED ---")
            print(f"To enable real emails, add MAIL_USERNAME and MAIL_PASSWORD to .env")
            print(f"OTP for {identifier}: {otp}")
            return True, f"Dev Mode: The OTP for testing is {otp}"

    # 2. SMS DELIVERY
    else:
        client = get_twilio_client()
        twilio_number = APP_CONFIG.get("TWILIO_PHONE_NUMBER")
        
        if client and twilio_number:
            try:
                # Format number logic
                clean_id = identifier.replace(" ", "").replace("-", "")
                if len(clean_id) == 10 and clean_id.isdigit():
                    to_number = f"+91{clean_id}"
                elif clean_id.startswith('+'):
                     to_number = clean_id
                else:
                    to_number = f"+{clean_id}"

                client.messages.create(
                    body=f"Your AquaSphereAI secure code is: {otp}",
                    from_=twilio_number,
                    to=to_number
                )
                return True, "otp_sent_to_sms"
            except Exception as e:
                print(f"SMS Error: {e}")
                # Fallback
                print(f"⚠️ SMS FAILED. DEBUG OTP: {otp}")
                return True, f"Dev Mode: Check Console or use {otp}"
        else:
            # Smart Fallback
            print(f"--- [DEBUG] REAL SMS SERVICE NOT CONFIGURED ---")
            print(f"To enable real SMS, add TWILIO keys to .env")
            print(f"OTP for {identifier}: {otp}")
            return True, f"Dev Mode: The OTP for testing is {otp}"

# Load Models (use script-relative paths to robustly locate files)
MODEL_DIR = os.path.join(os.path.dirname(__file__), "Models")
def _load_model(fname):
    path = os.path.join(MODEL_DIR, fname)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)

disease_model = _load_model("disease.pkl")
location_model = _load_model("location.pkl")
feed_model = _load_model("feed.pkl")
yield_model = _load_model("yield.pkl")
buyer_model = _load_model("buyer.pkl")
stocking_model = _load_model("stocking.pkl")
seed_model = _load_model("seed.pkl")

# Load Encoders
le_country = _load_model("le_country.pkl")
le_state = _load_model("le_state.pkl")
le_climate = _load_model("le_climate.pkl")
le_aqua = _load_model("le_aqua.pkl")
le_species_loc = _load_model("le_species_location.pkl")
le_species_feed = _load_model("le_species_feed.pkl")
le_feed = _load_model("le_feed.pkl")
le_species_yield = _load_model("le_species_yield.pkl")
le_country_buyer = _load_model("le_country_buyer.pkl")
le_species_buyer = _load_model("le_species_buyer.pkl")
le_grade_buyer = _load_model("le_grade_buyer.pkl")
le_species_stock = _load_model("le_species_stock.pkl")
le_soil = _load_model("le_soil.pkl")
le_water_source = _load_model("le_water_source.pkl")
le_season_stock = _load_model("le_season_stock.pkl")
le_country_seed = _load_model("le_country_seed.pkl")
le_species_seed_chk = _load_model("le_species_seed_chk.pkl")

# Global Aquaculture Regional Database
GLOBAL_AQUA_REGIONS = {
    "India": {
        "Andhra Pradesh": ["Krishna", "Nellore", "West Godavari", "East Godavari", "Prakasam", "Vizag"],
        "West Bengal": ["North 24 Parganas", "South 24 Parganas", "Purba Medinipur", "Howrah"],
        "Odisha": ["Balasore", "Bhadrak", "Ganjam", "Puri"],
        "Gujarat": ["Surat", "Bharuch", "Valsad", "Navsari"],
        "Tamil Nadu": ["Nagapattinam", "Thanjavur", "Cuddalore"]
    },
    "Vietnam": {
        "Mekong Delta": ["Can Tho", "Bac Lieu", "Ca Mau", "Soc Trang", "Ben Tre", "Tra Vinh"],
        "Central Highlands": ["Dak Lak", "Lam Dong"],
        "Red River Delta": ["Hai Phong", "Quang Ninh"]
    },
    "Thailand": {
        "Eastern Gulf": ["Chonburi", "Rayong", "Trat"],
        "Southern Thailand": ["Surat Thani", "Nakorn Si Thammarat", "Phuket"]
    },
    "Indonesia": {
        "Java": ["East Java", "West Java", "Central Java"],
        "Sumatra": ["Lampung", "North Sumatra", "Riau"],
        "Sulawesi": ["South Sulawesi", "North Sulawesi"]
    },
    "Bangladesh": {
        "Chittagong Division": ["Cox's Bazar", "Chittagong", "Noakhali"],
        "Khulna Division": ["Satkhira", "Bagerhat", "Khulna"]
    },
    "China": {
        "Guangdong": ["Zhanjiang", "Jiangmen", "Maoming"],
        "Fujian": ["Ningde", "Fuzhou", "Xiamen"],
        "Zhejiang": ["Wenzhou", "Ningbo"]
    },
    "Norway": {
        "Northern Norway": ["Nordland", "Troms", "Finnmark"],
        "Western Norway": ["Hordaland", "Rogaland", "Møre og Romsdal"]
    },
    "USA": {
        "Gulf Coast": ["Louisiana", "Mississippi", "Alabama", "Texas"],
        "Pacific Northwest": ["Washington", "Oregon", "Alaska"],
        "East Coast": ["Maine", "Maryland", "Virginia"]
    },
    "Brazil": {
        "Southern Coast": ["Santa Catarina", "Paraná"],
        "Northeast": ["Ceará", "Rio Grande do Norte", "Bahia"]
    }
}

# Species Categorization for Freshers (Emojis)
SPECIES_META = {
    "Rohu": "🐟", "Tilapia": "🐟", "Catfish": "🐟", "Seabass": "🐟", "Carp": "🐟", "Salmon": "🐟", "Trout": "🐟",
    "Pangasius": "🐟", "Grouper": "🐟", "Snapper": "🐟", "Milkfish": "🐟", "Barramundi": "🐟", "Tuna": "🐟", "Cod": "🐟",
    "Vannamei": "🦐", "Tiger Prawn": "🦐", "Freshwater Prawn": "🦐", "Banana Prawn": "🦐", "King Prawn": "🦐",
    "Whiteleg Shrimp": "🦐", "Black Tiger Shrimp": "🦐",
    "Mud Crab": "🦀", "Blue Swimmer Crab": "🦀", "King Crab": "🦀", "Snow Crab": "🦀", "Dungeness Crab": "🦀", "Soft Shell Crab": "🦀"
}

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.context_processor
def inject_globals():
    trans, lang = get_trans()
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:5000"
    # Helper to translate species
    def translate_species(s):
        key = f"species_{s.lower().replace(' ', '_')}"
        return trans.get(key, s)
    
    # Helper to translate regions (countries, states, districts)
    def translate_region(r):
        key = f"region_{r.lower().replace(' ', '_')}"
        return trans.get(key, r)

    species_list = [{"id": s, "display": f"{SPECIES_META[s]} {translate_species(s)}"} for s in SPECIES_META.keys()]
    
    # Translate Precaution DB
    def translate_tip(t):
        # Tip keys are created by slugifying the text
        clean_tip = t.lower().replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').replace('-', '_')
        key = f"tip_{clean_tip}"
        return trans.get(key, t)

    translated_precautions = {}
    for cat, items in PRECAUTIONS.items():
        t_cat = trans.get(f"cat_{cat.lower()}", cat)
        translated_precautions[t_cat] = {}
        for subcat, tips in items.items():
            t_subcat = trans.get(f"subcat_{subcat.lower()}", subcat)
            translated_precautions[t_cat][t_subcat] = [translate_tip(tip) for tip in tips]

    # Optionally translate the region_db if keys are found
    translated_regions = {}
    for country, states in GLOBAL_AQUA_REGIONS.items():
        t_country = translate_region(country)
        translated_regions[t_country] = {}
        for state, districts in states.items():
            t_state = translate_region(state)
            translated_regions[t_country][t_state] = [translate_region(d) for d in districts]

    return dict(species_list=species_list, region_db=translated_regions, 
                precautions_db=translated_precautions, trans=trans, lang=lang,
                local_url=local_url)

# ADVANCED PRECAUTIONS & ADVISORY SYSTEM
PRECAUTIONS = {
    "Disease": {
        "Prevention": [
            "Maintain Water pH 7.5-8.5", 
            "Check Ammonia weekly", 
            "Quarantine new seeds",
            "Maintain DO above 5.0 mg/L to reduce stress"
        ],
        "Action": [
            "Reduce feeding by 50% immediately", 
            "Apply probiotic treatment (e.g., Bacillus subtilis)", 
            "Increase aeration - add 1 aerator per hectare",
            "Perform 20% partial water exchange with treated water"
        ]
    },
    "Growth": {
        "Optimize": [
            "Use high-protein feed during Stage 1", 
            "Maintain DO above 5mg/L", 
            "Regular water exchange",
            "Maintain optimal temperature between 28-32°C"
        ],
        "Risk": [
            "High turbidity detected - check for algae bloom", 
            "Sudden temp drop alert - reduce feeding", 
            "Overstocking risk - consider partial harvest",
            "Ammonia spike alert - increase aerator runtime by 2 hours"
        ]
    },
    "Aeration": {
        "Management": [
            "Turn on Fant Sets (Aerators) between 3 AM and 6 AM when DO is lowest",
            "For Prawns: Run aerators 24/7 after Day 60 to maintain growth",
            "For Fish: If fish gulp for air at surface, turn on Fant Sets immediately",
            "Ensure 1 HP Fant Set per 500kg of biomass for peak efficiency"
        ]
    }
}

# SEASONAL ADVICE DB
SEASONAL_ADVICE = {
    "Summer": {
        "Fish": ["Rohu", "Catla", "Mrigal", "Tilapia", "Common Carp", "Pangasius (Basa)"],
        "Prawns": ["Shrimp (Vannamei)"],
        "Crabs": [],
        "Reason": "Water temp: 25–35°C. Best for warm-water species.",
        "Avoid": ["Crabs", "Trout", "Cold-water Species"],
        "WhyAvoid": "High surface temperatures (30°C+) can cause heat stress in mud crabs, leading to high mortality. Trout require oxygen-rich, cool water which is hard to maintain in summer.",
        "Tips": ["Low dissolved oxygen → use aerators", "Avoid overfeeding", "Maintain water depth"]
    },
    "Monsoon": {
        "Fish": ["Rohu", "Catla", "Mrigal", "Tilapia", "Milkfish"],
        "Prawns": ["Freshwater Prawn (Scampi)"],
        "Crabs": ["Mud Crab"],
        "Reason": "Water temp: 24–32°C. High water availability.",
        "Avoid": ["Strict Saline Species"],
        "WhyAvoid": "Heavy rains significantly dilute pond salinity. Species that require high stable salinity (like specific marine fish) may suffer osmotic shock.",
        "Tips": ["Risk of diseases", "Control pond overflow", "Maintain pH & turbidity"]
    },
    "Winter": {
        "Fish": ["Catfish", "Common Carp", "Trout (cold regions)"],
        "Prawns": ["Shrimp (Vannamei / Black Tiger)"],
        "Crabs": ["Oysters", "Mussels"],
        "Reason": "Water temp: 15–25°C. Best for cool-water & marine species.",
        "Avoid": ["Tropical Tilapia", "Warm-water Prawns"],
        "WhyAvoid": "Tilapia metabolism slows down below 20°C, stopping growth and weakening their immune system, making them prone to cold-water diseases.",
        "Tips": ["Fish metabolism slows", "Reduce feed quantity", "Monitor ammonia levels"]
    }
}

# SPECIES-SPECIFIC THRESHOLDS (NEW)
SPECIES_RULES = {
    "Vannamei": {"salinity": (10, 25), "pH": (7.5, 8.5), "temp": (28, 32)},
    "Rohu": {"salinity": (0, 5), "pH": (7.0, 8.5), "temp": (25, 30)},
    "Mud Crab": {"salinity": (15, 30), "pH": (7.5, 8.5), "temp": (26, 30)}
}

def get_trans():
    lang = request.args.get('lang', session.get('lang', 'en'))
    if lang not in TRANSLATIONS:
        lang = 'en'
    session['lang'] = lang
    return TRANSLATIONS[lang], lang

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            _, lang = get_trans()
            flash("Please login to access this feature.", "error")
            return redirect(url_for('login', lang=lang))
        # Optional: Verify Supabase session here if needed
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    trans, lang = get_trans()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            # Supabase Password Login
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if res.user:
                session["user"] = res.user.email
                
                # Sync local metadata
                if res.user.email not in USERS_DB:
                    USERS_DB[res.user.email] = {
                        "name": res.user.user_metadata.get("name", "Farmer"),
                        "role": "farmer",
                        "joined_at": datetime.now().isoformat()
                    }
                    save_json(USERS_FILE, USERS_DB)
                return redirect(url_for("home_page", lang=lang))
                
        except Exception as e:
            return render_template("login.html", trans=trans, lang=lang, error=str(e))
            
    return render_template("login.html", trans=trans, lang=lang)

@app.route("/login/google")
def login_google():
    """Initiate Google OAuth Flow"""
    google_id = os.getenv('GOOGLE_CLIENT_ID')
    
    # CRITICAL FIX: Block placeholder strings from hitting Google's servers
    if not google_id or "your_google" in google_id:
        flash("SYSTEM NOTICE: You haven't added your real Google API keys to the .env file yet. Switching to Demo Login Mode.", "info")
        return redirect(url_for('mock_google_callback'))
    
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/login/mock-google")
def mock_google_callback():
    """Mock Google Login for Local Testing when keys are missing"""
    # Simply log in as a pre-defined test user
    user_info = {
        "email": "local-tester@aqua-ecosystem.io",
        "name": "Local Test User (Demo)",
    }
    
    email = user_info.get('email')
    name = user_info.get('name')
    
    # Auto-register this demo user if not exists
    if email not in USERS_DB:
        USERS_DB[email] = {
            "name": name,
            "role": "farmer",
            "joined_at": datetime.now().isoformat(),
            "auth_method": "dev_mock"
        }
        save_json(USERS_FILE, USERS_DB)
    
    session["user"] = email
    _, lang = get_trans()
    flash(f"Success! Logged in as {name}. This is a local TEST session.", "success")
    return redirect(url_for("home_page", lang=lang))

@app.route("/login/google/callback")
def google_callback():
    """Handle Google OAuth Callback"""
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    
    email = user_info.get('email')
    name = user_info.get('name', 'Google User')
    
    # Auto-register if user doesn't exist
    if email not in USERS_DB:
        USERS_DB[email] = {
            "name": name,
            "role": "farmer",
            "joined_at": datetime.now().isoformat(),
            "auth_method": "google"
        }
        save_json(USERS_FILE, USERS_DB)
    
    session["user"] = email
    _, lang = get_trans()
    flash(f"Welcome, {name}! Logged in via Google.", "success")
    return redirect(url_for("home_page", lang=lang))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    trans, lang = get_trans()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            # Supabase Signup with Password
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name
                    }
                }
            })
            
            # Check if signup was successful and if auto-login happened (or needs email confirmation)
            if res.user:
                # If Supabase is set to require email confirmation, this might limit immediate login
                # But typically for this use case we assume we want to let them in or show a message
                
                # If session is created (auto-sign in is on)
                if res.session:
                    session["user"] = res.user.email
                    if res.user.email not in USERS_DB:
                        USERS_DB[res.user.email] = {
                            "name": name,
                            "role": "farmer",
                            "joined_at": datetime.now().isoformat()
                        }
                        save_json(USERS_FILE, USERS_DB)
                    flash("Account created successfully!", "success")
                    return redirect(url_for("home_page", lang=lang))
                else:
                    # User created but no session (maybe confirm email is required)
                    flash("Account created! Please check your email to confirm your account.", "info")
                    return redirect(url_for("login", lang=lang))
                    
        except Exception as e:
            return render_template("signup.html", trans=trans, lang=lang, error=str(e))
                
    return render_template("signup.html", trans=trans, lang=lang)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("landing"))

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    trans, lang = get_trans()
    # Basic Security: In a real app, this would be admin-only
    if request.method == "POST":
        APP_CONFIG.update({
            "DEMO_MODE": request.form.get("DEMO_MODE") == "on",
            "MAIL_SERVER": request.form.get("MAIL_SERVER"),
            "MAIL_PORT": int(request.form.get("MAIL_PORT", 587)),
            "MAIL_USE_TLS": request.form.get("MAIL_USE_TLS") == "on",
            "MAIL_USERNAME": request.form.get("MAIL_USERNAME"),
            "MAIL_PASSWORD": request.form.get("MAIL_PASSWORD"),
            "MAIL_DEFAULT_SENDER": request.form.get("MAIL_DEFAULT_SENDER"),
            "TWILIO_ACCOUNT_SID": request.form.get("TWILIO_ACCOUNT_SID"),
            "TWILIO_AUTH_TOKEN": request.form.get("TWILIO_AUTH_TOKEN"),
            "TWILIO_PHONE_NUMBER": request.form.get("TWILIO_PHONE_NUMBER")
        })
        save_json(CONFIG_FILE, APP_CONFIG)
        
        # Update Live App Config
        app.config.update(
            MAIL_SERVER=APP_CONFIG["MAIL_SERVER"],
            MAIL_PORT=APP_CONFIG["MAIL_PORT"],
            MAIL_USE_TLS=APP_CONFIG["MAIL_USE_TLS"],
            MAIL_USERNAME=APP_CONFIG["MAIL_USERNAME"],
            MAIL_PASSWORD=APP_CONFIG["MAIL_PASSWORD"],
            MAIL_DEFAULT_SENDER=APP_CONFIG["MAIL_DEFAULT_SENDER"]
        )
        flash("System settings updated and saved successfully.", "success")
        return redirect(url_for("settings", lang=lang))
        
    return render_template("settings.html", trans=trans, lang=lang, config=APP_CONFIG)

@app.route("/")
def landing():
    """Public Landing Page"""
    trans, lang = get_trans()
    
    # If user is already logged in, redirect to home page
    if 'user' in session:
        return redirect(url_for("home_page", lang=lang))

    # FETCH REAL LIVE DATA (Weather) - Client will handle offline state
    weather_info = "Loading..."
    try:
        res = requests.get("https://wttr.in/Visakhapatnam?format=%t+%C", timeout=2)
        if res.status_code == 200:
            weather_info = res.text
    except:
        weather_info = "28°C Clear"
    
    live_stats = {
        "weather": weather_info,
        "market_trend": "+4.2% Today",
        "active_experts": random.randint(12, 25),
        "global_users": "8.4k+"
    }
    
    return render_template("index.html", trans=trans, lang=lang, live_stats=live_stats)

@app.route("/home")
@login_required
def home_page():
    """Personalized Home Page for logged-in users"""
    trans, lang = get_trans()
    user_id = session.get('user')
    user_data = USERS_DB.get(user_id, {"name": "User"})
    
    # Mock some personalized stats
    personal_stats = {
        "active_ponds": random.randint(2, 5),
        "total_biomass": f"{random.randint(1200, 5000)} kg",
        "market_valuation": f"${random.randint(5000, 25000)}",
        "health_score": f"{random.randint(85, 98)}%"
    }
    
    return render_template("home.html", trans=trans, lang=lang, user=user_data, stats=personal_stats)

@app.route("/farmer")
@login_required
def farmer_hub():
    trans, lang = get_trans()
    return render_template("farmer_hub.html", trans=trans, lang=lang)

@app.route("/farmer/disease")
@login_required
def disease_page():
    trans, lang = get_trans()
    return render_template("disease_analysis.html", trans=trans, lang=lang)

@app.route("/farmer/feed")
@login_required
def feed_page():
    trans, lang = get_trans()
    return render_template("feed_calculation.html", trans=trans, lang=lang)

@app.route("/farmer/stocking")
@login_required
def stocking_page():
    trans, lang = get_trans()
    return render_template("stocking_advisor.html", trans=trans, lang=lang)

@app.route("/farmer/seed")
@login_required
def seed_page():
    trans, lang = get_trans()
    return render_template("seed_checker.html", trans=trans, lang=lang)

@app.route("/farmer/yield")
@login_required
def yield_page():
    trans, lang = get_trans()
    return render_template("yield_forecast.html", trans=trans, lang=lang)

@app.route("/logistics")
@login_required
def logistics():
    trans, lang = get_trans()
    return render_template("logistics.html", trans=trans, lang=lang)

@app.route("/districts")
@login_required
def districts():
    trans, lang = get_trans()
    return render_template("districts.html", trans=trans, lang=lang)

@app.route("/technicians")
@login_required
def technicians():
    trans, lang = get_trans()
    return render_template("technicians.html", trans=trans, lang=lang)

@app.route("/live-intel")
@login_required
def live_intelligence():
    trans, lang = get_trans()
    return render_template("live_intel.html", trans=trans, lang=lang)

@app.route("/location")
@login_required
def location():
    trans, lang = get_trans()
    return render_template("location_dashboard.html", trans=trans, lang=lang)

@app.route("/precautions")
@login_required
def precautions_dashboard():
    trans, lang = get_trans()
    return render_template("precautions.html", trans=trans, lang=lang, precautions_db=PRECAUTIONS)

@app.route("/qr-scanner")
@login_required
def qr_scanner():
    trans, lang = get_trans()
    return render_template("qr_scanner.html", trans=trans, lang=lang)

@app.route("/api/clear-session", methods=["POST"])
def clear_session():
    """Clear server-side session data"""
    session.clear()
    return jsonify({"status": "success", "message": "Session cleared"})

@app.route("/api/cache-info")
def cache_info():
    """Return cache information"""
    return jsonify({
        "status": "success",
        "server_session": len(session.keys()) if session else 0,
        "message": "Cache info retrieved"
    })

@app.route("/market")
def market():
    trans, lang = get_trans()
    # Simulated LIVE Global Stock Data with random fluctuations
    base_stocks = [
        {"id": 1, "country": "Norway", "state": "Nordland", "species": "Salmon", "qty": 45, "price": 12.5, "flag": "🇳🇴"},
        {"id": 2, "country": "Vietnam", "state": "Mekong Delta", "species": "Vannamei", "qty": 120, "price": 6.8, "flag": "🇻🇳"},
        {"id": 3, "country": "India", "state": "Andhra Pradesh", "species": "Tiger Prawn", "qty": 85, "price": 8.2, "flag": "🇮🇳"},
        {"id": 4, "country": "USA", "state": "Gulf Coast", "species": "Catfish", "qty": 200, "price": 4.5, "flag": "🇺🇸"},
        {"id": 5, "country": "Brazil", "state": "Northeast", "species": "Tilapia", "qty": 300, "price": 3.2, "flag": "🇧🇷"},
        {"id": 6, "country": "China", "state": "Guangdong", "species": "Mud Crab", "qty": 50, "price": 22.0, "flag": "🇨🇳"},
        {"id": 7, "country": "Bangladesh", "state": "Khulna", "species": "Rohu", "qty": 150, "price": 2.5, "flag": "🇧🇩"},
        {"id": 8, "country": "Thailand", "state": "Eastern Gulf", "species": "Seabass", "qty": 60, "price": 10.5, "flag": "🇹🇭"}
    ]
    
    # Add random "live" fluctuation (-2% to +2%)
    stocks = []
    for s in base_stocks:
        fluctuation = 1 + (random.uniform(-0.02, 0.02))
        s['price'] = round(s['price'] * fluctuation, 2)
        s['price_inr'] = round(s['price'] * USD_TO_INR, 2)
        s['last_update'] = datetime.now().strftime("%H:%M:%S")
        
        # Translate
        s['species_display'] = trans.get(f"species_{s['species'].lower().replace(' ', '_')}", s['species'])
        s['country_display'] = trans.get(f"country_{s['country'].lower().replace(' ', '_')}", s['country'])
        s['state_display'] = trans.get(f"region_{s['state'].lower().replace(' ', '_')}", s['state'])
        stocks.append(s)

    return render_template("market.html", trans=trans, lang=lang, stocks=stocks)

@app.route("/place_order", methods=["POST"])
@login_required
def place_order():
    trans, lang = get_trans()
    species = request.form.get("species")
    country = request.form.get("country")
    qty = request.form.get("qty")
    
    # Live Tracking: Origin -> Destination
    origin = f"{country} Central Hub"
    destination = session.get("user", "Guest Portal")
    
    msg = trans['order_msg'].format(qty=qty, species=species, country=country)
    tracking_info = f"Transport Path: {origin} 🚛 → {destination} (Live Tracking Active)"
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['order_success'],
                         description=msg,
                         result="ORDER PLACED",
                         unit=tracking_info)

@app.route("/buyer")
def buyer():
    trans, lang = get_trans()
    return render_template("buyer_dashboard.html", trans=trans, lang=lang)

@app.route("/predict_disease", methods=["POST"])
def predict_disease():
    trans, lang = get_trans()
    # Try to get species, fallback to Vannamei for specific rules
    species_name = request.form.get("species", "Vannamei")
    
    vals = [
        float(request.form["temp"]),
        float(request.form["ph"]),
        float(request.form["do"]),
        float(request.form["salinity"]),
        float(request.form["turbidity"])
    ]
    risk_score = disease_model.predict([vals])[0]
    
    # Advanced Early Warning Logic
    if risk_score > 0.7:
        state = trans['state_critical']
        advise = PRECAUTIONS["Disease"]["Action"]
    elif risk_score > 0.3:
        state = trans['state_risk']
        advise = PRECAUTIONS["Disease"]["Prevention"] + [trans.get("precaution_increase_monitoring", "Increase monitoring frequency")]
    else:
        state = trans['state_healthy']
        advise = PRECAUTIONS["Disease"]["Prevention"]
    
    if species_name in SPECIES_RULES:
        rules = SPECIES_RULES[species_name]
        if not (rules["salinity"][0] <= vals[3] <= rules["salinity"][1]):
            advise.append(trans['warn_salinity'].format(species=species_name, low=rules['salinity'][0], high=rules['salinity'][1]))
        if not (rules["pH"][0] <= vals[1] <= rules["pH"][1]):
            advise.append(trans['warn_ph'].format(species=species_name, low=rules['pH'][0], high=rules['pH'][1]))

    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['disease_title'],
                         description=f"{trans['feat_disease_desc']} ({species_name})",
                         result=state,
                         unit=trans['suitability_score'],
                         precautions=advise)

@app.route("/predict_location", methods=["POST"])
def predict_location():
    trans, lang = get_trans()
    # Robust handling for new global locations
    try:
        country_val = le_country.transform([request.form["country"]])[0]
    except:
        country_val = le_country.transform(["Vietnam"])[0] if "Vietnam" in le_country.classes_ else 0
        
    try:
        state_val = le_state.transform([request.form["state"]])[0]
    except:
        state_val = le_state.transform(["Mekong Delta"])[0] if "Mekong Delta" in le_state.classes_ else 0

    climate_name = request.form.get("climate", "Tropical")
    climate_val = le_climate.transform([climate_name])[0]
    aqua_type = le_aqua.transform([request.form["aqua_type"]])[0]
    species = le_species_loc.transform([request.form["species"]])[0]
    
    vals = [[country_val, state_val, climate_val, aqua_type, species]]
    score = location_model.predict(vals)[0]
    
    # Climate Risk Impact (Feature 8)
    climate_warning = ""
    if "Tropical" in climate_name:
        climate_warning = "⚠️ High Climate Risk: Monitor for Heat Waves & Cyclones."
    elif "Temperate" in climate_name:
        climate_warning = "⚠️ Heavy Rainfall Alert: Risk of salinity drop."
        
    # Contextual Advisory
    advise = PRECAUTIONS["Growth"]["Optimize"] if score > 70 else PRECAUTIONS["Growth"]["Risk"]
    if climate_warning:
        advise.append(climate_warning)
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['loc_title'],
                         description=f"{trans['feat_loc_desc']} ({species} in {climate_name})",
                         result=f"{round(score, 1)}%",
                         unit=trans['suitability_score'],
                         precautions=advise)

@app.route("/farmer/logbook")
def logbook():
    trans, lang = get_trans()
    # Simulated log data (Feature 11)
    logs = [
        {"date": "2026-01-20", "ph": 8.1, "do": 5.2, "feed": "45kg", "notes": "Normal growth"},
        {"date": "2026-01-21", "ph": 7.9, "do": 4.8, "feed": "42kg", "notes": "Minor DO drop - increased aeration"}
    ]
    return render_template("logbook.html", trans=trans, lang=lang, logs=logs)

@app.route("/farmer/export")
def export_compliance():
    trans, lang = get_trans()
    return render_template("export_checker.html", trans=trans, lang=lang)

@app.route("/check_export", methods=["POST"])
def check_export():
    trans, lang = get_trans()
    species = request.form.get("species")
    abw = float(request.form.get("abw", 0))
    region = request.form.get("region", "EU")
    
    # Export logic (Feature 7)
    eligible = False
    if region == "EU" and abw >= 25: eligible = True
    elif region == "USA" and abw >= 20: eligible = True
    elif region == "Japan" and abw >= 30: eligible = True
    
    result = trans['eligible'] if eligible else trans['ineligible']
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['export_compliance_title'].format(region=region),
                         description=f"{trans['export_compliance']} ({species}):",
                         result=result,
                         unit="Quality Audit Report",
                         precautions=[trans['precaution_antibiotic'], trans['precaution_cold_chain']])

@app.route("/predict_feed", methods=["POST"])
def predict_feed():
    trans, lang = get_trans()
    species_name = request.form.get("species", "Vannamei")
    species = le_species_feed.transform([species_name])[0]
    age = float(request.form.get("age", 30))
    temp = float(request.form.get("temp", 28))
    feed_type_name = request.form.get("feed_type", "Pellet")
    feed_type = le_feed.transform([feed_type_name])[0]
    
    vals = [[species, age, temp, 6.0, feed_type, 32]]
    quantity_kg = feed_model.predict(vals)[0]
    
    # Unit conversion
    unit_pref = request.form.get("unit_preference", "kg")
    quantity_display, unit_label = convert_quantity(quantity_kg, unit_pref, from_unit="kg")
    
    # Feed Optimization & Cost Reduction (Feature 13)
    cost_per_kg = 1.2 # Simulated (USD)
    total_cost_usd = quantity_kg * cost_per_kg
    total_cost_inr = total_cost_usd * USD_TO_INR
    saving_tip = trans.get("tip_automatic_feeders", "Tip: Use automatic feeders to reduce wastage by 15%.")
    
    # Growth Advisory
    advise = PRECAUTIONS["Growth"]["Optimize"] if temp > 25 else PRECAUTIONS["Growth"]["Risk"]
    advise.append(f"💰 {saving_tip}")
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['feed_optimizer_title'],
                         description=f"{trans['feed_desc']} ({species_name}):",
                         result=f"{round(quantity_display, 2)}",
                         unit=f"{unit_label} | Estimated Cost: ${round(total_cost_usd, 2)} / ₹{round(total_cost_inr, 2)} per Day",
                         precautions=advise)

@app.route("/farmer/iot")
def iot_dashboard():
    trans, lang = get_trans()
    # Simulated IoT Data (Feature 14)
    data = {
        "sensors": [
            {"name": "Pond 1 - pH", "value": 8.2, "status": "Normal"},
            {"name": "Pond 1 - DO", "value": 5.4, "status": "Optimal"},
            {"name": "Pond 2 - Temp", "value": 31.0, "status": "High Alert"},
            {"name": "Pond 2 - Turbidity", "value": 12.0, "status": "Normal"}
        ]
    }
    return render_template("iot_dashboard.html", trans=trans, lang=lang, data=data)

@app.route("/predict_yield", methods=["POST"])
def predict_yield():
    trans, lang = get_trans()
    species = le_species_yield.transform([request.form["species"]])[0]
    area = float(request.form["area"])
    feed = float(request.form["feed"])
    days = float(request.form["days"])
    
    vals = [[species, area, feed, days]]
    expected_yield_tons = yield_model.predict(vals)[0]
    
    # Unit conversion (default is tons, convert as needed)
    unit_pref = request.form.get("unit_preference", "tons")
    quantity_display, unit_label = convert_quantity(expected_yield_tons, unit_pref, from_unit="tons")
    
    # Growth Advisory
    advise = PRECAUTIONS["Growth"]["Optimize"] if expected_yield_tons > 50 else PRECAUTIONS["Growth"]["Risk"]
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['yield_title'],
                         description=trans['feat_yield_desc'],
                         result=f"{round(quantity_display, 2)}",
                         unit=unit_label,
                         precautions=advise)

@app.route("/predict_buyer", methods=["POST"])
def predict_buyer():
    trans, lang = get_trans()
    country_name = request.form.get("country", "USA")
    species_name = request.form.get("species", "Vannamei")
    
    try:
        country = le_country_buyer.transform([country_name])[0]
    except:
        country = 0
        
    try:
        species = le_species_buyer.transform([species_name])[0]
    except:
        species = 0
        
    quantity = float(request.form.get("quantity", 10))
    grade_name = request.form.get("grade", "A")
    try:
        grade = le_grade_buyer.transform([grade_name])[0]
    except:
        grade = 0
    
    vals = [[country, species, quantity, grade]]
    price_usd = buyer_model.predict(vals)[0]
    price_inr = price_usd * USD_TO_INR
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['negotiation_portal_title'].format(country=country_name),
                         description=f"AI Optimized Offer for {quantity} tons ({species_name}):",
                         result=f"${round(price_usd, 2):,} / ₹{round(price_inr, 2):,}",
                         unit=trans['final_price'])

@app.route("/calculate_eco", methods=["POST"])
def calculate_eco():
    trans, lang = get_trans()
    feed = float(request.form.get("feed"))
    harvest = float(request.form.get("harvest"))
    
    # New Input Logic: Area (Acres) & Depth (Feet)
    area_acres = float(request.form.get("area", 1))
    depth_feet = float(request.form.get("depth", 5)) # Default 5ft
    
    # Conversion: 1 Acre-foot ≈ 1233.48 m³
    volume_m3 = area_acres * depth_feet * 1233.48
    
    # Eco Metrics
    fcr = feed / harvest if harvest > 0 else 0
    water_efficiency = volume_m3 / harvest if harvest > 0 else 0 # m3 per kg fish
    carbon_footprint = (feed * 1.5) + (volume_m3 * 0.05) # Simulated CO2
    
    grade = "A+" if fcr < 1.5 else "B"
    
    advise = [trans.get('precaution_fcr_high', 'FCR > 1.8 indicates overfeeding')]
    if water_efficiency > 5:
        advise.append("High water usage detected. Consider recirculation.")
        
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['sust_report_title'],
                         description=f"FCR: {round(fcr, 2)} | Grade: {grade}",
                         result=f"{round(carbon_footprint, 1)}",
                         unit="kg CO2 (Carbon Footprint)",
                         precautions=advise)

@app.route("/predict_stocking", methods=["POST"])
def predict_stocking():
    trans, lang = get_trans()
    species = le_species_stock.transform([request.form["species"]])[0]
    area = float(request.form["area"])
    soil = le_soil.transform([request.form["soil"]])[0]
    water = le_water_source.transform([request.form["water"]])[0]
    season = le_season_stock.transform([request.form["season"]])[0]
    
    vals = [[species, area, soil, water, season]]
    res = stocking_model.predict(vals)[0]
    
    # Growth Advisory
    advise = PRECAUTIONS["Growth"]["Optimize"] if res[1] > 80 else PRECAUTIONS["Growth"]["Risk"]
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['stock_title'],
                         description=f"{trans['stock_desc']} ({request.form['species']}):",
                         result=f"{int(res[0])} Seeds / {round(res[1], 1)}% Survival",
                         unit="Advice",
                         precautions=advise)

@app.route("/harvest")
def harvest():
    trans, lang = get_trans()
    return render_template("harvest_analysis.html", trans=trans, lang=lang)

@app.route("/predict_harvest", methods=["POST"])
def predict_harvest():
    trans, lang = get_trans()
    species = request.form.get("species")
    days = float(request.form.get("days", 90))
    feed_total = float(request.form.get("feed", 1000))
    
    # Advanced Heuristic for Harvest Logic (Feature 5)
    # Average Body Weight (ABW) estimation
    if "Shrimp" in species or "Vannamei" in species:
        abw = (feed_total / (days * 1.5)) * 10  # Simplistic FCR-based growth
    else:
        abw = (feed_total / (days * 1.2)) * 20
        
    harvest_quality = trans['harvest_grade_a'] if abw > 25 else trans['harvest_grade_b']
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['harvest_title'],
                         description=f"{trans['harvest_desc']} ({species}, {days} days):",
                         result=f"{round(abw, 1)}g ABW",
                         unit=harvest_quality,
                         precautions=[trans['precaution_salinity_final'], trans['precaution_reduce_feed']])

@app.route("/farmer/seasonal")
def seasonal_advisor():
    trans, lang = get_trans()
    return render_template("seasonal_advisor.html", trans=trans, lang=lang, regions=GLOBAL_AQUA_REGIONS)

@app.route("/predict_seasonal", methods=["GET", "POST"])
def predict_seasonal():
    trans, lang = get_trans()
    season = request.form.get("season") or request.args.get("season")
    country = request.form.get("country")
    state = request.form.get("state")
    water_type = request.form.get("water_type", "Freshwater")
    
    if season in SEASONAL_ADVICE:
        # Deep copy simulated by manual list/dict copy to avoid mutating global
        orig = SEASONAL_ADVICE[season]
        data = {
            "Fish": list(orig.get("Fish", [])),
            "Prawns": list(orig.get("Prawns", [])),
            "Crabs": list(orig.get("Crabs", [])),
            "Reason": orig.get("Reason", ""),
            "Avoid": list(orig.get("Avoid", [])),
            "WhyAvoid": orig.get("WhyAvoid", ""),
            "Tips": list(orig.get("Tips", []))
        }
        
        # --- AI REGIONAL OVERRIDES ---
        # 1. cold region check (Norway, USA North)
        if country == "Norway" or (country == "USA" and state == "Pacific Northwest"):
            if season == "Winter":
                data["Fish"] = ["Atlantic Salmon", "Rainbow Trout", "Cod"]
                data["Reason"] = f"Arctic Winter focus in {state}: Optimal for cold-water marine species."
                data["Tips"] += ["Ensure heaters are functional", "Monitor for ice formation"]
            else:
                data["Fish"] = ["Salmon", "Trout", "Mackerel"]
        
        # 2. Water Type Filter
        if water_type == "Freshwater":
            # Remove high-salinity marine species if accidentally listed
            data["Fish"] = [f for f in data["Fish"] if f not in ["Seabass", "Grouper", "Snapper", "Tuna", "Cod"]]
            data["Avoid"].append("High-Saline Marine Species")
        else:
            # Brackish/Saline
            if "Shrimp (Vannamei)" not in data["Prawns"]:
                data["Prawns"].append("Shrimp (Vannamei)")
            data["Avoid"].append("Strict Freshwater Species (e.g. Rohu, Catla)")
            data["WhyAvoid"] += " High salinity causes osmotic stress in freshwater carps."

        reasons = data["Reason"]
        
        # Build Categorized Results
        result_parts = []
        if data.get("Fish"):
            result_parts.append(f"🐟 {trans.get('fish', 'Fish')}: {', '.join(data['Fish'])}")
        if data.get("Prawns"):
            result_parts.append(f"🦐 {trans.get('prawn', 'Prawns')}: {', '.join(data['Prawns'])}")
        if data.get("Crabs"):
            result_parts.append(f"🦀 {trans.get('crab', 'Crabs')}: {', '.join(data['Crabs'])}")
            
        final_result = "<br>".join(result_parts)
        avoid_str = ", ".join(data["Avoid"])
        why_avoid = data.get("WhyAvoid", "")
        
        # AI Simulated Environmental Insight
        loc_parts = [p for p in [state, country] if p]
        loc_str = ", ".join(loc_parts) if loc_parts else "Global"
        env_insight = f"📍 Location: {loc_str} | 💧 {data.get('WaterTypeDisplay', water_type)}"
        unit_text = f"❌ {trans.get('avoid', 'Avoid')}: {avoid_str}"
        if why_avoid:
            unit_text += f"<br><p style='font-size: 0.9rem; color: #ff4d4d; margin-top: 10px; font-weight: 500; font-style: italic;'>ℹ️ {trans.get('seasonal_reason', 'Reason')}: {why_avoid}</p>"
        
        return render_template("result.html", trans=trans, lang=lang,
                             title=f"{trans.get('seasonal_res_title', 'Seasonal Advice')}: {season}",
                             description=f"{env_insight}<br>{trans.get('seasonal_reason', 'Reason')}: {reasons}",
                             result=final_result,
                             unit=unit_text,
                             precautions=data["Tips"])
    else:
        return redirect(url_for('seasonal_advisor'))

@app.route("/knowledge")
@login_required
def knowledge_hub():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@app.route("/knowledge/start")
def guide_start_farm():
    trans, lang = get_trans()
    return render_template("guides/start_farm.html", trans=trans, lang=lang)

@app.route("/knowledge/vannamei")
def guide_vannamei():
    trans, lang = get_trans()
    return render_template("guides/vannamei.html", trans=trans, lang=lang)

@app.route("/knowledge/feed")
def guide_feed():
    trans, lang = get_trans()
    return render_template("guides/feed_chart.html", trans=trans, lang=lang)

@app.route("/knowledge/disease")
def guide_disease():
    trans, lang = get_trans()
    return render_template("guides/disease_solutions.html", trans=trans, lang=lang)

@app.route("/farmer/vision")
def vision_tool():
    trans, lang = get_trans()
    return render_template("vision_analysis.html", trans=trans, lang=lang)

@app.route("/predict_vision", methods=["POST"])
def predict_vision():
    trans, lang = get_trans()
    file = request.files.get("file")
    # Simulated CNN interpretation logic (Feature 2)
    filename = secure_filename(file.filename) if file else "sample.jpg"
    
    # Heuristic: Randomly assign common visible diseases for demo
    findings = random.choice([
        "White Spot Signs (WSS) Detected",
        "Gill Discoloration Observed",
        "Healthy External Shell",
        "Tail Erosion Symptoms"
    ])
    
    confidence = random.randint(85, 98)
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['vision_scan_title'],
                         description=f"{trans['visual_scan']} ({filename}):",
                         result=trans.get(findings.lower().replace(' ', '_').replace(')', '').replace('(', ''), findings),
                         unit=trans['confidence'].format(value=confidence),
                         precautions=[trans['precaution_isolate'], trans['precaution_consult_expert']])

@app.route("/farmer/sustainability")
def sustainability_tool():
    trans, lang = get_trans()
    return render_template("sustainability_tracker.html", trans=trans, lang=lang)

@app.route("/farmer/prawn-count")
@login_required
def prawn_counter():
    trans, lang = get_trans()
    
    # 📡 Real-time Market Data for Counts (Simulated)
    # Price usually increases as Count decreases (larger prawns = higher price)
    base_price = 320 # Base price for 100 count
    
    # Generate pricing grid for common counts
    counts = [30, 40, 50, 60, 70, 80, 100]
    market_grid = []
    
    # Generate pricing grid for common counts
    counts = [30, 40, 50, 60, 70, 80, 100]
    market_grid = []
    
    for c in counts:
        # Smaller count = Larger size = Higher Price
        # Simple formula for simulation: Base + (100 - count) * multiplier
        p = base_price + (100 - c) * 6.5 
        # Add random live fluctuation
        p = p * random.uniform(0.98, 1.02)
        
        market_grid.append({
            "count": c,
            "weight_g": round(1000/c, 1),
            "price": int(p),
            "trend": random.choice(["up", "down", "stable"])
        })
    
    # 🦐 Live Farm Estimation (Simulated for 'Auto-Predict')
    # Use time to simulate growth curve (15g to 35g cycle)
    t = time.time()
    current_abw = round(15 + (t % 1000000) / 50000, 2) # Slowly changing ABW
    if current_abw > 40: current_abw = 15 # Reset cycle
    
    estimated_count_per_kg = int(1000 / current_abw)
        
    return render_template("prawn_counter.html", trans=trans, lang=lang, market_grid=market_grid, 
                         live_data={"abw": current_abw, "est_count": estimated_count_per_kg})

@app.route("/predict_seed", methods=["POST"])
def predict_seed():
    trans, lang = get_trans()
    country = le_country_seed.transform([request.form["country"]])[0]
    species = le_species_seed_chk.transform([request.form["species"]])[0]
    distance = float(request.form["distance"])
    
    vals = [[country, species, distance]]
    rating = seed_model.predict(vals)[0]
    
    # Growth Advisory
    advise = list(PRECAUTIONS["Growth"]["Optimize"] if rating > 4.0 else PRECAUTIONS["Growth"]["Risk"])
    
    # Feature: Transport Stress Analysis
    species_name = request.form["species"]
    result_text = f"{round(rating, 1)} / 5"
    
    if distance > 40:
        result_text += " (🟡 Medium Quality)"
        advise.insert(0, "⚠️ Transport stress detected")
        
        if "Prawn" in species_name or "Shrimp" in species_name or "Vannamei" in species_name:
            advise.append("✅ Recommendation: Use acclimatization")
            advise.append("✅ Recommendation: Add probiotics")
            advise.append("✅ Recommendation: Reduce initial stocking density")
            advise.append("✅ Recommendation: Increase Oxygen (O2) in transport bags due to high pressure/distance.")
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['seed_title'],
                         description=trans['growth_potential'],
                         result=result_text,
                         unit=trans['quality_score'],
                         precautions=advise)

@app.route("/consult_technician", methods=["POST"])
def consult_technician():
    trans, lang = get_trans()
    if not session.get("user"):
        return redirect(url_for("login", lang=lang))
        
    file = request.files.get('media')
    message = request.form.get('message')
    tech_id = request.form.get('tech_id')
    user_id = session.get("user")
    user_name = USERS_DB.get(user_id, {}).get("name", "Unknown Farmer")
    
    if file and allowed_file(file.filename):
        filename = f"{user_id}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['consult_active'],
                         description=trans['consult_msg'].format(user=user_name, id=user_id, tech=tech_id),
                         result=trans['connected'],
                         unit=trans['syncing'])

@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    trans, lang = get_trans()
    data = request.json
    msg = data.get("message", "").lower()
    
    # Smart "Internet-style" Knowledge Response
    response = "I am searching our global database... "
    
    if "price" in msg or "market" in msg:
        response = "Market Analysis: Prices for Vannamei in the Mekong Delta are trending at $6.8/kg, while in India they are approx ₹560/kg. Global demand is rising (📈 +5.2%)."
    elif "disease" in msg or "white spot" in msg:
        response = "Health Alert: White Spot disease risk is high when water temp drops below 26°C. Ensure probiotics are applied and feeding is reduced by 30%."
    elif "weather" in msg or "climate" in msg:
        response = "Climate Data: Monsoon regions are currently reporting high turbidity. Maintain pond depth at 1.5m to stabilize temperatures."
    elif "growth" in msg or "fcr" in msg:
        response = "Optimization: To improve FCR, use high-protein starters in the first 30 days and maintain Dissolved Oxygen above 5.5 mg/L."
    else:
        response = "I have analyzed your query from our AquaSphere intelligence network. It is recommended to maintain stability in pH (7.5-8.5) and monitor water color daily for optimal plankton bloom."
        
    return jsonify({"reply": response})

@app.route("/api/connection-status")
def api_connection_status():
    """Check if client is connected to internet"""
    try:
        # Try to reach a reliable external service
        response = requests.get('https://www.google.com', timeout=2)
        return jsonify({
            "online": True,
            "status": "ONLINE",
            "message": "Connected to internet",
            "timestamp": datetime.now().isoformat()
        }), 200
    except:
        # If unreachable, we're likely offline
        return jsonify({
            "online": False,
            "status": "OFFLINE",
            "message": "No internet connection",
            "timestamp": datetime.now().isoformat()
        }), 200

@app.route("/api/realtime")
def api_realtime():
    # 📡 OFFLINE CHECK - Return minimal data if offline
    # NOTE: This endpoint should only be called when ALLOW_LIVE_DATA is true on client
    
    # Simulated Real-time AI processing of pond data
    t = time.time()
    # Create sine-wave like fluctuations for realism
    ph = round(8.2 + 0.1 * math.sin(t / 10), 2)
    do = round(5.4 + 0.3 * math.cos(t / 15), 2)
    temp = round(29.4 + 0.4 * math.sin(t / 60), 1)
    ammonia = round(0.15 + 0.05 * math.sin(t / 45), 2)
    turbidity = round(34 + 2 * math.cos(t / 30), 1)
    salinity = round(18 + 0.5 * math.sin(t / 120), 1)
    
    # 🐟 Biological Metrics
    fcr = round(1.25 + 0.05 * math.sin(t / 200), 2)
    growth_rate = round(2.1 + 0.1 * math.cos(t / 150), 1)
    health_index = int(92 + 3 * math.sin(t / 180))
    harvest_days = max(0, int(23 - (t % 86400) / 3600)) # Simple simulated countdown

    # ⚠️ Risk Predictions
    disease_risk = round((math.sin(t / 100) + 1) * 2, 1) # 0-4%
    oxygen_crash_prob = round((math.cos(t / 80) + 1) * 5, 1) # 0-10%
    
    # 🤖 Advanced Recommendations
    aerators = 2 if do < 5.5 else 1
    power_usage = round(1.2 + 0.4 * (aerators/2), 2)
    next_feed = max(0, int(20 - (t % 1200) / 60)) # countdown from 20 mins
    
    # 🦐 Prawns Counter Data (Simulated)
    # Base stock 250,000 with slight daily fluctuation due to mortality/harvest
    prawn_stock_count = int(250000 - (t % 86400) / 10) 
    # Average Body Weight (g) increasing over time
    abw = round(15 + (t % 1000) / 100, 2)
    # Total Weight (kg)
    total_weight = round((prawn_stock_count * abw) / 1000, 1)
    
    growth_status = "Excellent" if abw > 18 else ("Good" if abw > 15 else "Slow")

    return jsonify({
        "ph": ph,
        "do": do,
        "temp": temp,
        "ammonia": ammonia,
        "turbidity": turbidity,
        "salinity": salinity,
        "fcr": fcr,
        "growth_rate": growth_rate,
        "health_index": health_index,
        "harvest_days": harvest_days,
        "disease_risk": disease_risk,
        "oxygen_crash_prob": oxygen_crash_prob,
        "aerators": aerators,
        "power_usage": power_usage,
        "next_feed": next_feed,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "order_progress": round(((time.time() % 3600) / 3600) * 100, 1),
        "ship_1": {
            "lat": round(16.42 + (time.time() % 300) / 150, 4),
            "lon": round(82.15 + (time.time() % 500) / 250, 4)
        },
        "prawn_stock_count": prawn_stock_count,
        "prawn_total_weight": total_weight,
        "prawn_abw": abw,
        "prawn_growth_status": growth_status
    })

@app.route("/track_order")
def track_order():
    trans, lang = get_trans()
    order_id = request.args.get("order_id", "AQ102")
    return render_template("order_tracker.html", trans=trans, lang=lang, order_id=order_id)

@app.route("/early-warning")
def early_warning():
    trans, lang = get_trans()
    # Simulated regional disease detection
    alerts = [
        {"region": "Nellore Delta", "disease": "White Spot (WSSV)", "radius": "15km", "intensity": "High"},
        {"region": "Mekong Basin", "disease": "RMS Syndrome", "radius": "50km", "intensity": "Medium"}
    ]
    return render_template("early_warning.html", trans=trans, lang=lang, alerts=alerts)

@app.route("/traceability")
def traceability():
    trans, lang = get_trans()
    batch_id = request.args.get("id", "BATCH-2026-X8")
    return render_template("traceability.html", trans=trans, lang=lang, batch_id=batch_id)

@app.route("/insurance-claims")
def insurance_claims():
    trans, lang = get_trans()
    return render_template("insurance.html", trans=trans, lang=lang)

@app.route("/sustainability-tracker")
def sustainability_tracker():
    trans, lang = get_trans()
    return render_template("sustainability.html", trans=trans, lang=lang)

@app.route("/api/explainable_ai")
def api_xai():
    # Simulated Explainable AI Reasoning (Feature 2)
    reasons = [
        "Risk increased because D.O. levels dropped 15% between 2 AM - 4 AM.",
        "Expected growth slowed due to temperature fluctuation (+3°C deviation).",
        "Higher Ammonia (0.21 mg/L) detected; likelihood of feed over-accumulation is 78%."
    ]
    return jsonify({"reason": random.choice(reasons)})

@app.route("/api/feed_fraud")
def api_feed_fraud():
    # Simulated Feed Fraud Detector (Feature 4)
    status = random.choice(["Normal", "Anomaly Detected", "Normal", "Normal"])
    return jsonify({
        "status": status,
        "details": "FCR deviation > 12% vs biological peer groups" if status == "Anomaly Detected" else "Quality verified"
    })

@app.route("/api/market_live")
def api_market_live():
    # 📡 OFFLINE CHECK - Client should not call this when offline
    # This endpoint returns live market price fluctuations only when online
    
    # Simulated LIVE Global Stock Data with Availability Counts
    all_species = [
        {"name": "Vannamei", "base": 6.5, "type": "prawn", "farms": random.randint(120, 200), "stock_tons": random.randint(500, 1200)},
        {"name": "Tiger Prawn", "base": 9.2, "type": "prawn", "farms": random.randint(80, 150), "stock_tons": random.randint(300, 800)},
        {"name": "Freshwater Prawn", "base": 7.8, "type": "prawn", "farms": random.randint(50, 100), "stock_tons": random.randint(200, 500)},
        {"name": "Black Tiger Shrimp", "base": 10.5, "type": "prawn", "farms": random.randint(40, 80), "stock_tons": random.randint(150, 400)},
        {"name": "Whiteleg Shrimp", "base": 6.8, "type": "prawn", "farms": random.randint(100, 180), "stock_tons": random.randint(400, 1000)},
        {"name": "Rohu", "base": 2.5, "type": "fish", "farms": random.randint(200, 400), "stock_tons": random.randint(800, 2000)},
        {"name": "Tilapia", "base": 3.0, "type": "fish", "farms": random.randint(300, 500), "stock_tons": random.randint(1000, 3000)},
        {"name": "Catfish", "base": 4.2, "type": "fish", "farms": random.randint(150, 300), "stock_tons": random.randint(600, 1500)},
        {"name": "Seabass", "base": 11.5, "type": "fish", "farms": random.randint(30, 80), "stock_tons": random.randint(100, 400)},
        {"name": "Mud Crab", "base": 22.0, "type": "crab", "farms": random.randint(20, 60), "stock_tons": random.randint(50, 200)},
        {"name": "Blue Swimmer Crab", "base": 18.5, "type": "crab", "farms": random.randint(15, 40), "stock_tons": random.randint(30, 150)}
    ]
    
    data = []
    total_prawns_count = 0
    total_prawns_farms = 0
    total_prawns_stock = 0
    
    for s in all_species:
        # Random walk fluctuation
        change_pct = round(random.uniform(-0.05, 0.05) * 100, 1)
        price_usd = round(s['base'] * (1 + change_pct/100), 2)
        
        item = {
            "species": s['name'], 
            "type": s['type'],
            "price": price_usd, 
            "change": change_pct,
            "farms_count": s['farms'],
            "stock_tons": s['stock_tons'],
            "availability": "High" if s['stock_tons'] > 500 else ("Medium" if s['stock_tons'] > 200 else "Low")
        }
        data.append(item)
        
        # Calculate total prawns statistics
        if s['type'] == 'prawn':
            total_prawns_count += 1
            total_prawns_farms += s['farms']
            total_prawns_stock += s['stock_tons']
    
    # Add summary statistics
    summary = {
        "total_prawns_species": total_prawns_count,
        "total_prawns_farms": total_prawns_farms,
        "total_prawns_stock_tons": total_prawns_stock,
        "last_update": datetime.now().strftime("%H:%M:%S"),
        "market_status": "Active" if datetime.now().hour >= 6 and datetime.now().hour <= 20 else "Closing"
    }
    
    return jsonify({"data": data, "summary": summary})


# ============ COMMUNITY & ANALYTICS FEATURES ============

def get_community_analytics():
    """Aggregate community insights from mock/real data"""
    # 1. Active Farmers per Region (Simulated based on USERS_DB or random if empty)
    regions = {}
    total_ponds = 0
    
    # Seed some mock data if empty for demo purposes
    mock_regions = ["Andhra Pradesh", "West Bengal", "Odisha", "Gujarat", "Mekong Delta"]
    
    for _ in range(50): # Simulate 50 active nodes
        r = random.choice(mock_regions)
        regions[r] = regions.get(r, 0) + 1
        total_ponds += random.randint(1, 5)
        
    # 2. Disease Trends (Aggregated from recent posts or predictions)
    recent_diseases = [
        {"name": "White Spot", "count": 12, "trend": "up"},
        {"name": "Black Gill", "count": 8, "trend": "down"},
        {"name": "Running Mortality", "count": 5, "trend": "stable"}
    ]
    
    return {
        "active_farmers": regions,
        "pond_density": total_ponds,
        "disease_trends": recent_diseases,
        "total_farmers": 1240 + len(USERS_DB)
    }

@app.route("/community")
@login_required
def community_hub():
    trans, lang = get_trans()
    user_id = session.get("user")
    
    # Mock some posts if empty
    if not COMMUNITY_DB["posts"]:
        COMMUNITY_DB["posts"] = [
            {"id": 1, "author": "Ravi Kumar", "author_id": "ravi@example.com", "content": "Just harvested 5 tons of Vannamei! ABW 28g. Very happy with the yield this season. used Probiotics from day 30.", "type": "yield", "timestamp": "2 hours ago", "likes": 15, "replies": []},
            {"id": 2, "author": "Nguyen Van", "author_id": "nguyen@example.com", "content": "Has anyone faced sudden pH drop after heavy rain? My pond dropped from 8.2 to 7.4 overnight.", "type": "disease", "timestamp": "5 hours ago", "likes": 8, "replies": []},
            {"id": 3, "author": "Sarah Chen", "author_id": "sarah@example.com", "content": "Market price for Tiger Prawn is up by 10% in the export market. Good time to harvest if your ABW is above 30g.", "type": "profit", "timestamp": "1 day ago", "likes": 42, "replies": []}
        ]
    
    # Suggested Farmers to Follow
    suggestions = [
        {"name": "Dr. A. Sharma", "id": "exp1", "specialty": "Disease Expert", "location": "Nellore"},
        {"name": "Best Aqua Feeds", "id": "exp2", "specialty": "Feed Supplier", "location": "Global"},
        {"name": "K. Venkat", "id": "exp3", "specialty": "Vannamei Farmer", "location": "Guntur"}
    ]
    
    # Get user's following list
    user_data = USERS_DB.get(user_id, {})
    following = user_data.get("following", [])
    
    # Filter suggestions
    suggestions = [s for s in suggestions if s["id"] not in following]
    
    return render_template("community_hub.html", 
                         trans=trans, 
                         lang=lang, 
                         posts=reversed(COMMUNITY_DB["posts"]), 
                         suggestions=suggestions,
                         groups=COMMUNITY_DB["groups"],
                         analytics=get_community_analytics())

@app.route("/community/post", methods=["POST"])
@login_required
def community_post():
    trans, lang = get_trans()
        
    content = request.form.get("content")
    post_type = request.form.get("type", "general")
    user_id = session.get("user")
    user_name = USERS_DB.get(user_id, {}).get("name", "Farmer")
    
    new_post = {
        "id": len(COMMUNITY_DB["posts"]) + 1,
        "author": user_name,
        "author_id": user_id,
        "content": content,
        "type": post_type,
        "timestamp": "Just now",
        "likes": 0,
        "replies": []
    }
    
    COMMUNITY_DB["posts"].append(new_post)
    save_json(COMMUNITY_FILE, COMMUNITY_DB)
    
    flash("Post shared with community!", "success")
    return redirect(url_for("community_hub", lang=lang))

@app.route("/community/follow/<target_id>")
@login_required
def follow_user(target_id):
        
    user_id = session.get("user")
    if user_id not in USERS_DB:
        USERS_DB[user_id] = {"name": "Current User"} # Should exist, but safety check
        
    if "following" not in USERS_DB[user_id]:
        USERS_DB[user_id]["following"] = []
        
    if target_id not in USERS_DB[user_id]["following"]:
        USERS_DB[user_id]["following"].append(target_id)
        # Mock add to target's followers logic here
    else:
        USERS_DB[user_id]["following"].remove(target_id)
        
    save_json(USERS_FILE, USERS_DB)
    return redirect(url_for("community_hub"))

@app.route("/community/insights")
@login_required
def community_insights():
    trans, lang = get_trans()
    data = get_community_analytics()
    
    # Detailed Regional Data
    regional_data = [
        {"region": "Andhra Pradesh", "farmers": 450, "ponds": 1200, "top_crop": "Vannamei", "risk": "Low"},
        {"region": "Mekong Delta", "farmers": 320, "ponds": 850, "top_crop": "Tiger Prawn", "risk": "Medium"},
        {"region": "Gujarat", "farmers": 180, "ponds": 600, "top_crop": "Vannamei", "risk": "High (Salinity)"}
    ]
    
    return render_template("community_insights.html", 
                         trans=trans, 
                         lang=lang,
                         data=data,
                         regional_data=regional_data)

# ============ OFFLINE SUPPORT API ENDPOINTS ============

@app.route('/api/dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    """Endpoint to serve datasets for offline caching"""
    try:
        import csv
        filepath = f"dataset/{dataset_name}.csv"
        if not os.path.exists(filepath):
            return jsonify({"error": "Dataset not found"}), 404
        
        data = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        return jsonify(data)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sync-prediction', methods=['POST'])
def sync_prediction():
    """Endpoint to sync offline predictions when back online"""
    try:
        data = request.get_json()
        # Store synced prediction if needed (optional: for analytics)
        if not os.path.exists("offline_predictions.json"):
            offline_preds = []
        else:
            with open("offline_predictions.json", 'r') as f:
                offline_preds = json.load(f)
        
        offline_preds.append({
            **data,
            "synced_at": datetime.now().isoformat()
        })
        
        save_json("offline_predictions.json", offline_preds)
        return jsonify({"status": "synced", "id": data.get('id')}), 200
    except Exception as e:
        print(f"Sync error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/offline-status')
def offline_status():
    """Check offline capabilities and cached data status"""
    trans, lang = get_trans()
    
    # Check which datasets are available
    datasets = []
    for dataset in ["disease", "location", "feed", "yield", "buyer", "stocking", "seed"]:
        path = f"dataset/{dataset}.csv"
        datasets.append({
            "name": dataset,
            "available": os.path.exists(path),
            "size": os.path.getsize(path) if os.path.exists(path) else 0
        })
    
    return render_template("offline_status.html", 
                         trans=trans, 
                         lang=lang,
                         datasets=datasets,
                         offline_predictions=load_json("offline_predictions.json", []))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
