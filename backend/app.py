# AQUA - Smart Aquaculture Platform with AI-Powered Predictions
# ==============================================================
# 
# CUSTOM HYBRID MACHINE LEARNING ALGORITHMS:
# -------------------------------------------
# This application uses proprietary hybrid algorithms developed specifically for aquaculture prediction tasks.
# For detailed algorithm documentation, see: ALGORITHMS_DOCUMENTATION.md

from flask import Flask, session
from flask_mail import Mail  # type: ignore
from dotenv import load_dotenv  # type: ignore
from twilio.rest import Client  # type: ignore

import os
import socket
from supabase import create_client  # type: ignore
from flask_cors import CORS

from core.translations import TRANSLATIONS
from core.ecosystem_config import AQUA_ROLES, AQUACYCLE_CONNECTIONS, AQUA_ROLE_ACTIONS, ROLE_MAP
from core.db import APP_CONFIG
from core.auth_utils import get_trans
from core.knowledge_base import PRECAUTIONS, GLOBAL_AQUA_REGIONS, SPECIES_META

load_dotenv()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Allow http for local OAuth

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

app = Flask(__name__, 
            template_folder=os.path.join(FRONTEND_DIR, 'templates'),
            static_folder=os.path.join(FRONTEND_DIR, 'static'))
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "aqua_secret_key_CHANGE_IN_PROD")
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Register Blueprints
from routes.farmer import farmer_bp
from routes.business import business_bp
from routes.voice import voice_bp
from routes.auth import auth_bp
from routes.vision import vision_bp
from routes.main import main_bp
from routes.aquacycle import aquacycle_bp
from routes.ai_predictions import ai_bp
from routes.finance import finance_bp
from routes.expert import expert_bp
from routes.buyer import buyer_bp
from routes.hatchery import hatchery_bp
from routes.lab_tech import lab_tech_bp
from routes.logistics import logistics_bp
from routes.global_intel import global_intel_bp
from routes.compliance import compliance_bp
from routes.satellite import satellite_bp
from routes.carbon_credits import carbon_credits_bp
from routes.broodstock import broodstock_bp
from routes.equipment import equipment_bp
from routes.consultant import consultant_bp
from routes.harvest import harvest_bp
from routes.cold_storage import cold_storage_bp
from routes.processing import processing_bp
from routes.certifier import certifier_bp
from routes.exporter import exporter_bp
from routes.retailer import retailer_bp
from routes.bank import bank_bp

app.register_blueprint(farmer_bp)
app.register_blueprint(business_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(vision_bp)
app.register_blueprint(main_bp)
app.register_blueprint(aquacycle_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(expert_bp)
app.register_blueprint(buyer_bp)
app.register_blueprint(hatchery_bp)
app.register_blueprint(lab_tech_bp)
app.register_blueprint(logistics_bp)
app.register_blueprint(global_intel_bp)
app.register_blueprint(compliance_bp)
app.register_blueprint(satellite_bp)
app.register_blueprint(carbon_credits_bp)
app.register_blueprint(broodstock_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(consultant_bp)
app.register_blueprint(harvest_bp)
app.register_blueprint(cold_storage_bp)
app.register_blueprint(processing_bp)
app.register_blueprint(certifier_bp)
app.register_blueprint(exporter_bp)
app.register_blueprint(retailer_bp)
app.register_blueprint(bank_bp)

# Supabase Initialization
from core.supabase_client import supabase, is_mock

UPLOAD_FOLDER = os.path.join(FRONTEND_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
except:
    pass

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
from core.oauth_client import oauth
oauth.init_app(app)

def check_services():
    supa_url = os.getenv('SUPABASE_URL', '')
    mail_user = os.getenv('MAIL_USERNAME', '')
    return {
        "google": not is_mock,
        "email": bool(mail_user and "your-email" not in mail_user),
        "sms": bool(os.getenv('TWILIO_ACCOUNT_SID') and "your_twilio" not in os.getenv('TWILIO_ACCOUNT_SID', '')),
        "env_file": os.path.exists('.env')
    }

@app.context_processor
def inject_service_status():
    return dict(service_status=check_services())

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

@app.context_processor
def inject_globals():
    from ml_core.models_loader import get_global_prices
    trans, lang = get_trans()
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:5000"
    def translate_species(s): return trans.get(f"species_{s.lower().replace(' ', '_')}", s)
    def translate_region(r): return trans.get(f"region_{r.lower().replace(' ', '_')}", r)
    def translate_tip(t):
        clean_tip = t.lower().replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').replace('-', '_')
        return trans.get(f"tip_{clean_tip}", t)

    species_list = [{"id": s, "display": f"{SPECIES_META[s]} {translate_species(s)}"} for s in SPECIES_META.keys()]
    
    translated_precautions = {}
    for cat, items in PRECAUTIONS.items():
        t_cat = trans.get(f"cat_{cat.lower()}", cat)
        translated_precautions[t_cat] = {}
        for subcat, tips in items.items():
            t_subcat = trans.get(f"subcat_{subcat.lower()}", subcat)
            translated_precautions[t_cat][t_subcat] = [translate_tip(tip) for tip in tips]

    translated_regions = {}
    for country, states in GLOBAL_AQUA_REGIONS.items():
        t_country = translate_region(country)
        translated_regions[t_country] = {}
        for state, districts in states.items():
            t_state = translate_region(state)
            translated_regions[t_country][t_state] = [translate_region(d) for d in districts]

    translated_roles = {}
    for rid, rdata in AQUA_ROLES.items():
        translated_roles[rid] = {
            "id": rid,
            "name": trans.get(f"role_{rid}", rdata["name"]),
            "icon": rdata["icon"],
            "category": trans.get(f"cat_{rdata['category'].lower()}", rdata["category"])
        }

    return dict(species_list=species_list, region_db=translated_regions,
                precautions_db=translated_precautions, trans=trans, lang=lang,
                local_url=local_url, app_online=True, config=APP_CONFIG,
                aqua_roles=translated_roles, get_global_prices=get_global_prices)

if __name__ == "__main__":
    if not os.path.exists('data'): os.makedirs('data')
    app.run(debug=True, host="0.0.0.0", port=5000)
