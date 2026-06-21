from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
import requests
import random
from core.auth_utils import get_trans, role_required, login_required
from core.db import AQUACYCLE_DB, APP_CONFIG, USERS_DB, EXPERTS_DB, save_json, CONFIG_FILE
from core.ecosystem_config import AQUA_ROLES, AQUACYCLE_CONNECTIONS
from core.knowledge_base import PRECAUTIONS, GLOBAL_AQUA_REGIONS

main_bp = Blueprint('main', __name__)

@main_bp.route("/api/set-lang-by-geo", methods=["POST"])
def set_lang_by_geo():
    data = request.get_json() or {}
    lat = data.get('lat')
    lon = data.get('lon')
    
    detected = 'en'
    
    if lat and lon:
        if 13.5 < lat < 19.5 and 76.5 < lon < 84.5: detected = 'te'
        elif 8.0 < lat < 13.5 and 76.0 < lon < 80.5: detected = 'ta'
        elif 21.5 < lat < 27.0 and 85.5 < lon < 89.5: detected = 'bn'
        elif 20.0 < lat < 24.5 and 68.5 < lon < 74.5: detected = 'gu'
        elif 8.0 < lat < 13.0 and 74.5 < lon < 77.5: detected = 'ml'
        elif 11.5 < lat < 18.5 and 74.0 < lon < 78.5: detected = 'kn'
        elif 17.5 < lat < 22.5 and 81.0 < lon < 87.5: detected = 'or'
        elif 15.5 < lat < 20.5 and 72.5 < lon < 80.5: detected = 'mr'
        elif 8.0 < lat < 37.0 and 68.0 < lon < 97.0: detected = 'hi'
    
    else:
        try:
            user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ',' in user_ip: user_ip = user_ip.split(',')[0]
            
            geo_res = requests.get(f"http://ip-api.com/json/{user_ip}?fields=status,countryCode,regionName", timeout=2)
            if geo_res.status_code == 200:
                geo_data = geo_res.json()
                if geo_data.get('status') == 'success':
                    region = geo_data.get('regionName', '').lower()
                    country = geo_data.get('countryCode', '')
                    
                    if country == 'IN':
                        if 'andhra' in region or 'telangana' in region: detected = 'te'
                        elif 'tamil' in region: detected = 'ta'
                        elif 'west bengal' in region: detected = 'bn'
                        elif 'gujarat' in region: detected = 'gu'
                        elif 'kerala' in region: detected = 'ml'
                        elif 'karnataka' in region: detected = 'kn'
                        elif 'odisha' in region: detected = 'or'
                        elif 'maharashtra' in region: detected = 'mr'
                        else: detected = 'hi'
                    elif country == 'ES': detected = 'es'
                    elif country == 'FR': detected = 'fr'
                    elif country == 'CN': detected = 'zh'
                    elif country == 'VN': detected = 'vi'
                    elif country == 'ID': detected = 'id'
                    elif country == 'TH': detected = 'th'
        except Exception as e:
            print(f"GeoIP Fallback Error: {e}")

    if 'detected_lang' not in session or session['detected_lang'] != detected:
        session['detected_lang'] = detected
        if 'manual_lang' not in session:
            session['lang'] = detected
            return jsonify({"status": "updated", "lang": detected})
            
    return jsonify({"status": "no_change", "lang": session.get('lang', 'en')})

@main_bp.route("/profile")
@login_required
def profile_page():
    trans, lang = get_trans()
    return render_template("profile.html", trans=trans, lang=lang)

@main_bp.route("/ledger")
def ledger_hub():
    return render_template("ledger.html")

@main_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    trans, lang = get_trans()
    if request.method == "POST":
        APP_CONFIG.update({
            "DEMO_MODE": request.form.get("DEMO_MODE") == "on",
            "MAIL_SERVER": request.form.get("MAIL_SERVER"),
            "MAIL_PORT": int(request.form.get("MAIL_PORT", 587)),
            "MAIL_USE_TLS": request.form.get("MAIL_USE_TLS") == "on",
            "MAIL_USERNAME": request.form.get("MAIL_USERNAME"),
            "MAIL_PASSWORD": request.form.get("MAIL_PASSWORD"),
            "MAIL_DEFAULT_SENDER": request.form.get("MAIL_DEFAULT_SENDER"),
            "TWILIO_PHONE_NUMBER": request.form.get("TWILIO_PHONE_NUMBER"),
            "FEATURES": {
                "AI_CHATBOT": request.form.get("FEAT_AI_CHATBOT") == "on",
                "NEURAL_TICKER": request.form.get("FEAT_NEURAL_TICKER") == "on",
                "PAYMENT_TRANSFERS": request.form.get("FEAT_PAYMENT_TRANSFERS") == "on",
                "DISEASE_ANALYSIS": request.form.get("FEAT_DISEASE_ANALYSIS") == "on",
                "LOCATION_ADVISOR": request.form.get("FEAT_LOCATION_ADVISOR") == "on",
                "MARKET_MATRIX": request.form.get("FEAT_MARKET_MATRIX") == "on"
            }
        })
        save_json(CONFIG_FILE, APP_CONFIG)
        
        # Avoid direct app.config update here, to avoid circular import. App handles this via APP_CONFIG reference.
        flash("System settings updated and saved successfully.", "success")
        return redirect(url_for("main.settings", lang=lang))
        
    return render_template("settings.html", trans=trans, lang=lang, config=APP_CONFIG)

@main_bp.route("/api/user-status")
def api_user_status():
    if 'user' in session:
        return jsonify({
            "status": "success",
            "user": {
                "email": session["user"],
                "name": session["user_name"],
                "role": session["role"],
                "pic": session["user_pic"]
            }
        })
    return jsonify({"status": "guest"})

@main_bp.route("/api/landing")
def api_landing():
    trans, lang = get_trans()
    weather_info = "28°C Clear"
    try:
        res = requests.get("https://wttr.in/Visakhapatnam?format=%t+%C", timeout=2)
        if res.status_code == 200: weather_info = res.text
    except: pass
    
    live_stats = {
        "weather": weather_info,
        "market_trend": "+4.2% Today",
        "active_experts": random.randint(12, 25),
        "global_users": "8.4k+"
    }
    return jsonify({"status": "success", "trans": trans, "lang": lang, "live_stats": live_stats})

@main_bp.route("/")
def landing():
    res = api_landing().get_json()
    if 'user' in session:
        return redirect(url_for("main.dashboard"))
    import json
    return render_template("index.html", 
                           trans=res['trans'], 
                           lang=res['lang'], 
                           live_stats=res['live_stats'],
                           roles_json=json.dumps(AQUA_ROLES),
                           connections_json=json.dumps(AQUACYCLE_CONNECTIONS),
                           user_role="admin")

@main_bp.route("/api/home")
@login_required
def api_home_data():
    trans, lang = get_trans()
    user_id = session.get('user')
    user_data = USERS_DB.get(user_id, {"name": "User", "role": "farmer"})
    
    personal_stats = {
        "active_ponds": random.randint(2, 5),
        "total_biomass": f"{random.randint(1200, 5000)} kg",
        "market_valuation": f"${random.randint(5000, 25000)}",
        "health_score": f"{random.randint(85, 98)}%"
    }
    return jsonify({
        "status": "success",
        "user": {
            "name": user_data.get("name"),
            "role": user_data.get("role"),
            "pic": user_data.get("picture")
        },
        "stats": personal_stats,
        "experts": EXPERTS_DB[:5]
    })

@main_bp.route("/home")
@login_required
def home_page():
    res = api_home_data().get_json()
    trans, lang = get_trans()
    return render_template("home.html", trans=trans, lang=lang, user=res['user'], stats=res['stats'], experts=EXPERTS_DB, aqua_roles=AQUA_ROLES)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Will call the api_aquacycle_dashboard function if needed, but since it's a blueprint we can just redirect or request it.
    from routes.aquacycle import api_aquacycle_dashboard
    api_res = api_aquacycle_dashboard().get_json()
    if api_res.get('status') == 'error':
        flash(api_res.get('message', 'Access Denied'), "error")
        return redirect(url_for("main.home_page"))
        
    trans, lang = get_trans()
    return render_template("dashboard.html", 
                         trans=trans, 
                         lang=lang, 
                         dashboard_data=api_res['data'],
                         aqua_roles=AQUA_ROLES)

@main_bp.route("/ecosystem")
@main_bp.route("/portal")
@main_bp.route("/expert")
@main_bp.route("/business")
def ecosystem():
    import json
    trans, lang = get_trans()
    user_role = session.get("role", "farmer")
    
    connections = AQUACYCLE_CONNECTIONS.get(user_role, [])
    recommendations = []
    for role_id in connections:
        if role_id in AQUA_ROLES:
            info = AQUA_ROLES[role_id]
            recommendations.append({
                "id": role_id,
                "name": info["name"],
                "icon": info["icon"],
                "role": info["category"],
                "location": "Global Hub"
            })
            
    return render_template("ecosystem.html",
                           trans=trans,
                           lang=lang,
                           roles_json=json.dumps(AQUA_ROLES),
                           connections_json=json.dumps(AQUACYCLE_CONNECTIONS),
                           user_role=user_role,
                           recommendations=recommendations)

@main_bp.route("/districts")
@role_required(['farmer', 'admin'])
def districts():
    trans, lang = get_trans()
    return render_template("districts.html", trans=trans, lang=lang)

@main_bp.route("/smart-matcher")
@login_required
def smart_matcher():
    trans, lang = get_trans()
    return render_template("smart_matcher.html", trans=trans, lang=lang)

@main_bp.route("/technicians")
@role_required(['farmer', 'admin'])
def technicians():
    trans, lang = get_trans()
    return render_template("technicians.html", trans=trans, lang=lang)

@main_bp.route("/live-intel")
@role_required(['farmer', 'admin'])
def live_intelligence():
    trans, lang = get_trans()
    return render_template("live_intel.html", trans=trans, lang=lang)

@main_bp.route("/location")
@role_required(['farmer', 'admin'])
def location():
    trans, lang = get_trans()
    return render_template("location_dashboard.html", trans=trans, lang=lang)

@main_bp.route("/precautions")
@role_required(['farmer', 'admin'])
def precautions_dashboard():
    trans, lang = get_trans()
    return render_template("precautions.html", trans=trans, lang=lang, precautions_db=PRECAUTIONS)

@main_bp.route("/qr-scanner")
@role_required(['farmer', 'admin'])
def qr_scanner():
    trans, lang = get_trans()
    return render_template("qr_scanner.html", trans=trans, lang=lang)

@main_bp.route("/api/clear-session", methods=["POST"])
def clear_session():
    session.clear()
    return jsonify({"status": "success", "message": "Session cleared"})

@main_bp.route("/api/cache-info")
def cache_info():
    return jsonify({
        "status": "success",
        "server_session": len(session.keys()) if session else 0,
        "message": "Cache info retrieved"
    })

@main_bp.route("/farmer/logbook")
def logbook():
    trans, lang = get_trans()
    logs = [
        {"date": "2026-01-20", "ph": 8.1, "do": 5.2, "feed": "45kg", "notes": "Normal growth"},
        {"date": "2026-01-21", "ph": 7.9, "do": 4.8, "feed": "42kg", "notes": "Minor DO drop - increased aeration"}
    ]
    return render_template("logbook.html", trans=trans, lang=lang, logs=logs)

@main_bp.route("/farmer/export")
def export_compliance():
    trans, lang = get_trans()
    return render_template("export_checker.html", trans=trans, lang=lang)

@main_bp.route("/farmer/iot")
def iot_dashboard():
    trans, lang = get_trans()
    data = {
        "sensors": [
            {"name": "Pond 1 - pH", "value": 8.2, "status": "Normal"},
            {"name": "Pond 1 - DO", "value": 5.4, "status": "Optimal"},
            {"name": "Pond 2 - Temp", "value": 31.0, "status": "High Alert"},
            {"name": "Pond 2 - Turbidity", "value": 12.0, "status": "Normal"}
        ],
        "recent_activity": random.sample([
            {"msg": "Satellite Link: Zone-4 Sync Complete", "time": "Just Now"},
            {"msg": "Market Price: Vannamei UP 0.5%", "time": "2 mins ago"},
            {"msg": "Water Tech: Sensor Node-12 Active", "time": "5 mins ago"},
            {"msg": "Logistics: Batch B-4421 Dispatched", "time": "12 mins ago"},
            {"msg": "System: Neural Optimization Active", "time": "15 mins ago"},
            {"msg": "Expert: Dr. Rao shared new insight", "time": "20 mins ago"},
            {"msg": "Alert: Salinity shift in Pond-2", "time": "25 mins ago"},
            {"msg": "Weather: Rain predicted in 4 hours", "time": "30 mins ago"}
        ], 4),
    }
    return render_template("iot_dashboard.html", trans=trans, lang=lang, data=data)

@main_bp.route("/harvest")
def harvest():
    trans, lang = get_trans()
    return render_template("harvest_analysis.html", trans=trans, lang=lang)

@main_bp.route("/farmer/seasonal")
@role_required(['farmer', 'admin'])
def seasonal_advisor():
    trans, lang = get_trans()
    return render_template("seasonal_advisor.html", trans=trans, lang=lang, regions=GLOBAL_AQUA_REGIONS)

@main_bp.route("/knowledge")
@login_required
def knowledge_hub():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/start")
def guide_start_farm():
    trans, lang = get_trans()
    return render_template("guides/start_farm.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/vannamei")
def guide_vannamei():
    trans, lang = get_trans()
    return render_template("guides/vannamei.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/fish")
def guide_fish():
    trans, lang = get_trans()
    return render_template("guides/fish.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/crab")
def guide_crab():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/mollusk")
def guide_mollusk():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/feed")
def guide_feed():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@main_bp.route("/knowledge/disease")
def guide_disease():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@main_bp.route("/community")
def community():
    trans, lang = get_trans()
    return render_template("community.html", trans=trans, lang=lang)

@main_bp.route("/trade")
def direct_trade():
    trans, lang = get_trans()
    return render_template("trade.html", trans=trans, lang=lang)

@main_bp.route("/admin")
@role_required(['admin'])
def admin_dashboard():
    trans, lang = get_trans()
    
    from ml_core.models_loader import get_global_prices, USD_TO_INR
    
    def multi_curr(inr_amount_str):
        inr_val = float(inr_amount_str.replace(",", ""))
        usd_val = inr_val / USD_TO_INR
        prices = get_global_prices(usd_val)
        return f"${prices['USD']} / ₹{prices['INR']} / €{prices['EUR']}"

    stats = {
        "total_users": len(USERS_DB),
        "new_users_today": 5,
        "total_revenue": multi_curr("12,45,000"),
        "revenue_growth": 14,
        "active_sessions": 124,
        "total_orders": 450,
        "orders_value": multi_curr("8,50,000")
    }
    
    role_dist = {}
    for user in USERS_DB.values():
        role = user.get('role', 'farmer')
        role_dist[role] = role_dist.get(role, 0) + 1
        
    revenue_streams = [
        {"name": "Trade Commission", "amount": multi_curr("8,50,000"), "percent": 68},
        {"name": "Premium Subscriptions", "amount": multi_curr("2,45,000"), "percent": 20},
        {"name": "Logistics Fees", "amount": multi_curr("1,50,000"), "percent": 12}
    ]
    
    recent_activity = [
        {"icon": "🚀", "message": "New export batch dispatched", "time": "2 mins ago", "value": multi_curr("4,50,000")},
        {"icon": "🛡️", "message": "System integrity check passed", "time": "10 mins ago", "value": ""},
        {"icon": "👥", "message": "New expert onboarded", "time": "1 hour ago", "value": ""}
    ]
    
    revenue = {
        "today": multi_curr("45,000"),
        "today_txns": 124,
        "month": multi_curr("12,45,000"),
        "month_growth": 14,
        "total": multi_curr("1,45,00,000")
    }
    
    transactions = [
        {"icon": "💸", "description": "Trade Settlement", "user": "farmer@aqua.com", "method": "Bank Transfer", "time": "5 mins ago", "type": "credit", "amount": multi_curr("1,20,000"), "status": "Completed"},
        {"icon": "💳", "description": "Subscription Fee", "user": "business@aqua.com", "method": "Card", "time": "1 hour ago", "type": "credit", "amount": multi_curr("5,000"), "status": "Completed"}
    ]
    
    services = [
        {"name": "Core Database", "details": "Latency: 24ms", "status": "green"},
        {"name": "AI Vision Engine", "details": "Load: 45%", "status": "green"},
        {"name": "Payment Gateway", "details": "Sync Delayed", "status": "yellow"},
        {"name": "IoT Data Sync", "details": "Latency: 18ms", "status": "green"}
    ]
    
    admin_config = {
        "maintenance": False,
        "platform_upi": "aquasphere@upi",
        "commission_rate": 2.5,
        "free_limit": 50
    }
    
    platform_alerts = [
        {"level": "critical", "icon": "⚠️", "title": "Payment Sync Issue", "message": "Delayed settlement from banking partner.", "time": "10 mins ago"},
        {"level": "warning", "icon": "🌡️", "title": "High API Load", "message": "Weather API latency spike detected.", "time": "1 hour ago"}
    ]

    return render_template("admin_dashboard.html", 
                           trans=trans, 
                           lang=lang,
                           stats=stats,
                           role_dist=role_dist,
                           revenue_streams=revenue_streams,
                           recent_activity=recent_activity,
                           users=USERS_DB,
                           revenue=revenue,
                           transactions=transactions,
                           services=services,
                           admin_config=admin_config,
                           platform_alerts=platform_alerts)

# --- NEW: TIER 2 GAME CHANGERS ---

@main_bp.route("/api/ussd", methods=["POST"])
def api_ussd_mode():
    data = request.get_json(silent=True) or request.form
    ussd_string = data.get("ussd_string", "*123#")
    
    # Mocking USSD logic for feature phones
    if ussd_string == "*123*1#":
        msg = "Pond 1 Status: DO=4.5, pH=7.8. Alert: DO dropping. Start Aerator."
    elif ussd_string == "*123*2#":
        msg = "Market: Vannamei 40C = Rs. 380/kg. Up by Rs 10 today."
    else:
        msg = "AQUA Menu:\n1. Pond Status\n2. Market Prices\n3. Weather Alert\nReply 1, 2, or 3."
        
    return jsonify({
        "status": "success",
        "ussd_response": msg,
        "format": "SMS-Plaintext"
    })

@main_bp.route("/aqualearn")
@login_required
def aqualearn_page():
    trans, lang = get_trans()
    return render_template("aqualearn.html", trans=trans, lang=lang)

@main_bp.route("/marketplace")
@login_required
def marketplace_page():
    trans, lang = get_trans()
    return render_template("marketplace.html", trans=trans, lang=lang)

@main_bp.route("/api/family-mode/switch", methods=["POST"])
@login_required
def api_family_mode_switch():
    data = request.get_json(silent=True) or {}
    new_role = data.get("role", "farmer")
    
    # Mock switching between family members on the same account
    session['role'] = new_role
    role_names = {
        "farmer": "Father (Pond Monitor)",
        "business": "Son (Marketplace)",
        "admin": "Daughter (Finances)"
    }
    
    return jsonify({
        "status": "success",
        "message": f"Switched profile to {role_names.get(new_role, new_role)}",
        "new_role": new_role
    })

# --- NEW: TIER 3 SMART ADDITIONS ---

@main_bp.route("/global-prices")
@login_required
def global_prices_page():
    trans, lang = get_trans()
    return render_template("global_prices.html", trans=trans, lang=lang)

@main_bp.route("/api/aquabot", methods=["POST"])
def api_aquabot():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").lower()
    lang = data.get("lang", "te") # Default Telugu mock
    
    # Simple Mock NLP for AquaBot Voice Assistant
    if "oxygen" in query or "ela" in query:
        response_text = "Mee pond lo oxygen level 4.2 undi. Idi thakkuva. Ventane aerator on cheyandi."
        audio_mock = "/static/audio/aquabot_oxygen_te.mp3"
    elif "price" in query or "dara" in query:
        response_text = "Ee roju vannamei dara 380 rupayalu. Market peruguthundi."
        audio_mock = "/static/audio/aquabot_price_te.mp3"
    else:
        response_text = "Naku ardham kaledu, malli cheppandi."
        audio_mock = ""
        
    return jsonify({
        "status": "success",
        "bot_response": response_text,
        "audio_url": audio_mock,
        "transcribed_query": query,
        "detected_language": lang
    })


