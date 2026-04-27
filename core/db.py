import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash  # type: ignore

# File paths for persistence (Organized in data/ folder)
USERS_FILE = 'data/users.json'
CONFIG_FILE = 'data/config.json'
COMMUNITY_FILE = 'data/community.json'
AQUACYCLE_FILE = 'data/aquacycle.json'
AQUAVISION_FILE = 'data/aquavision.json'
FEEDBACK_FILE = 'data/feedback.json'
INVITE_FILE = 'data/invites.json'

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

AQUACYCLE_DB = load_json(AQUACYCLE_FILE, {
    "leads": [
        {"id": "L1", "from": "farmer", "to": "feed_supplier", "msg": "Request: 5 Tons of High-Protein Feed (Vannamei 35%)", "status": "pending"},
        {"id": "L2", "from": "hatchery", "to": "transport", "msg": "Urgent: Temp-controlled transport for 2M PL", "status": "active"},
        {"id": "L3", "from": "exporter", "to": "farmer", "msg": "Buy Order: Vannamei 40-count @ $6.8/kg (10 Tons)", "status": "open"},
        {"id": "L4", "from": "farmer", "to": "lab_tech", "msg": "Request: Disease screening for Pond #4", "status": "pending"},
        {"id": "L5", "from": "processing_plant", "to": "processing_plant", "msg": "Inspection: Batch #BT-992 processing started", "status": "active"},
        {"id": "L6", "from": "admin", "to": "hatchery", "msg": "Notice: Quarterly hygiene audit scheduled", "status": "pending"},
        {"id": "L7", "from": "buyer", "to": "buyer", "msg": "Stock Request: 500kg Fresh Tiger Prawns", "status": "pending"},
        {"id": "L8", "from": "admin", "to": "farmer", "msg": "Alert: Loan application L-882 approved", "status": "active"},
        {"id": "L9", "from": "farmer", "to": "harvest_contractor", "msg": "Service: Harvest team needed for 15th March", "status": "pending"}
    ],
    "reports": [
        {"id": "R1", "from": "lab_tech", "to": "farmer", "title": "Water Analysis: Pond #2 (pH 7.8, Amm: 0.1)", "date": "2026-03-08"},
        {"id": "R2", "from": "lab_tech", "to": "farmer", "title": "Protocol: Early Mortality Syndrome prevention", "date": "2026-03-07"},
        {"id": "R3", "from": "processing_plant", "to": "processing_plant", "title": "QC Pass: Export Batch #V-102 (Grade A)", "date": "2026-03-08"},
        {"id": "R4", "from": "processing_plant", "to": "exporter", "title": "Inventory: Shelf-life analysis Report", "date": "2026-03-06"}
    ],
    "hatcheries": {}, 
    "seed_batches": [], 
    "farms": {}, 
    "ponds": [], 
    "inventory": [], 
    "shipments": [], 
    "jobs": [], 
    "finance": {"loans": [], "insurance": []},
    "transactions": []
})
def save_aquacycle(): save_json(AQUACYCLE_FILE, AQUACYCLE_DB)

AQUAVISION_DB = load_json(AQUAVISION_FILE, {
    "trained_weights": {"accuracy": 94.2, "samples": 13600, "last_trained": "2026-03-09"},
    "custom_labels": {}
})
def save_aquavision(): save_json(AQUAVISION_FILE, AQUAVISION_DB)

FEEDBACK_DB = load_json(FEEDBACK_FILE, [])
def save_feedback(): save_json(FEEDBACK_FILE, FEEDBACK_DB)

INVITE_DB = load_json(INVITE_FILE, {
    "active_codes": ["AQUA-BETA-2026", "AQUA-PILOT-01"],
    "used_by": {}
})
def save_invites(): save_json(INVITE_FILE, INVITE_DB)

USERS_DB = load_json(USERS_FILE, {})

# Auto-create default admin account
if 'admin@aquasphere.com' not in USERS_DB:
    USERS_DB['admin@aquasphere.com'] = {
        "name": "AquaSphere Admin",
        "password": generate_password_hash("admin123"),
        "role": "admin",
        "joined_at": datetime.now().isoformat(),
        "auth_method": "local",
        "picture": ""
    }
    save_json(USERS_FILE, USERS_DB)
    print("✅ Default admin account initialized in core/db.")

# ---- EXPERT & MARKET DB EXTENSIONS ----
ORDERS_FILE = 'data/orders.json'
EXPERTS_FILE = 'data/experts.json'
PAYMENTS_FILE = 'data/payments.json'
ADMIN_CONFIG_FILE = 'data/admin_config.json'
SESSIONS_FILE = 'data/sessions.json'
PROBLEMS_FILE = 'data/problems.json'

ORDERS_DB = load_json(ORDERS_FILE, [])
EXPERTS_DB = load_json(EXPERTS_FILE, [
    {"id": "exp1", "name": "Dr. Anil Sharma", "emoji": "👨‍🔬", "specialty": "Disease & Health Management", "bio": "20+ years in aquaculture disease diagnosis. Specialized in shrimp pathology and WSSV management.", "rating": 5, "reviews": 142, "rate": 800, "location": "Nellore, AP", "verified": True, "online": True, "upi_id": "anil@hdfc"},
    {"id": "exp2", "name": "Dr. Chen Wei", "emoji": "🔬", "specialty": "Water Quality & Chemistry", "bio": "Marine biologist with expertise in brackish water aquaculture and water chemistry optimization.", "rating": 4, "reviews": 89, "rate": 600, "location": "Guangdong, China", "verified": True, "online": False, "upi_id": "chen@axis"},
    {"id": "exp3", "name": "K. Venkatesh", "emoji": "🌾", "specialty": "Feed Management & Nutrition", "bio": "Senior aquaculture lab_tech specializing in FCR optimization and feed cost reduction strategies.", "rating": 5, "reviews": 213, "rate": 500, "location": "Guntur, AP", "verified": True, "online": True, "upi_id": "venkat@paytm"},
    {"id": "exp4", "name": "Priya Nair", "emoji": "💼", "specialty": "Market & Trade Consulting", "bio": "10 years in aquaculture export. Helps farmers get best prices and navigate export compliance.", "rating": 4, "reviews": 67, "rate": 700, "location": "Kochi, Kerala", "verified": True, "online": False, "upi_id": "priya@gpay"},
    {"id": "exp5", "name": "Nguyen Thi Lan", "emoji": "🌊", "specialty": "General Aquaculture", "bio": "Vannamei farming expert from Mekong Delta with 15 years experience in intensive farming.", "rating": 5, "reviews": 178, "rate": 450, "location": "Can Tho, Vietnam", "verified": True, "online": True, "upi_id": "lan@bhim"},
])
PAYMENTS_DB = load_json(PAYMENTS_FILE, [])
ADMIN_CONFIG = load_json(ADMIN_CONFIG_FILE, {
    "maintenance": False,
    "platform_upi": "aquasphere@hdfcbank",
    "commission_rate": 15,
    "free_limit": 20,
    "startup_name": "AquaSphere AI",
    "startup_founded": "2025"
})
SESSIONS_DB = load_json(SESSIONS_FILE, [])
PROBLEMS_DB = load_json(PROBLEMS_FILE, [])

def save_orders(): save_json(ORDERS_FILE, ORDERS_DB)
def save_experts(): save_json(EXPERTS_FILE, EXPERTS_DB)
def save_payments(): save_json(PAYMENTS_FILE, PAYMENTS_DB)
def save_sessions(): save_json(SESSIONS_FILE, SESSIONS_DB)
def save_admin_config(): save_json(ADMIN_CONFIG_FILE, ADMIN_CONFIG)
def save_problems(): save_json(PROBLEMS_FILE, PROBLEMS_DB)

# ---- COMMUNITY & CONFIG DB ----
COMMUNITY_DB = load_json(COMMUNITY_FILE, {
    "posts": [],
    "groups": ["General", "Disease Management", "Market Trends", "Yield Optimization"],
    "user_groups": {}  # user_id -> [list of groups]
})

DIRECT_TRADE_FILE = 'data/direct_trade.json'
DIRECT_TRADE_DB = load_json(DIRECT_TRADE_FILE, {
    "farmer_listings": [],
    "company_tenders": [
        {"id": "T-101", "company": "AquaGlobal Ltd", "need": "Vannamei Shrimp", "count": "30/40", "qty": "50 Tons", "urgency": "High", "location": "Andhra Pradesh", "icon": "🛰️"},
        {"id": "T-102", "company": "SeaFood Exp", "need": "Tiger Prawn", "count": "20/30", "qty": "20 Tons", "urgency": "Normal", "location": "Gujarat", "icon": "🚢"},
        {"id": "T-103", "company": "Delta Frozen", "need": "Mud Crab", "count": "N/A", "qty": "5 Tons", "urgency": "High", "location": "Kerala", "icon": "🦀"}
    ],
    "messages": []
})
def save_direct_trade(): save_json(DIRECT_TRADE_FILE, DIRECT_TRADE_DB)

APP_CONFIG = load_json(CONFIG_FILE, {
    "DEMO_MODE": False,
    "MAIL_SERVER": os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    "MAIL_PORT": int(os.getenv('MAIL_PORT', 587)),
    "MAIL_USE_TLS": os.getenv('MAIL_USE_TLS', 'True') == 'True',
    "MAIL_USERNAME": os.getenv('MAIL_USERNAME', ''),
    "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD', ''),
    "MAIL_DEFAULT_SENDER": os.getenv('MAIL_DEFAULT_SENDER', ''),
    "TWILIO_PHONE_NUMBER": os.getenv('TWILIO_PHONE_NUMBER', ''),
    "FEATURES": {
        "AI_CHATBOT": True,
        "NEURAL_TICKER": True,
        "PAYMENT_TRANSFERS": True,
        "DISEASE_ANALYSIS": True,
        "LOCATION_ADVISOR": True,
        "MARKET_MATRIX": True
    }
})

DEFAULT_FEATURES = {
    "AI_CHATBOT": True,
    "NEURAL_TICKER": True,
    "PAYMENT_TRANSFERS": True,
    "DISEASE_ANALYSIS": True,
    "LOCATION_ADVISOR": True,
    "MARKET_MATRIX": True
}
if "FEATURES" not in APP_CONFIG:
    APP_CONFIG["FEATURES"] = DEFAULT_FEATURES
    save_json(CONFIG_FILE, APP_CONFIG)
else:
    changed = False
    for k, v in DEFAULT_FEATURES.items():
        if k not in APP_CONFIG["FEATURES"]:  # pyre-ignore
            APP_CONFIG["FEATURES"][k] = v  # pyre-ignore
            changed = True
    if changed:
        save_json(CONFIG_FILE, APP_CONFIG)
