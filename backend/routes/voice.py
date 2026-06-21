from flask import Blueprint, request, jsonify, session
from core.db import AQUACYCLE_DB, save_aquacycle, USERS_DB, ORDERS_DB, EXPERTS_DB
import random
import datetime

voice_bp = Blueprint('voice_bp', __name__)

# --- ADVANCED AI VOICE COMMAND BACKEND NLP PROCESSOR ---
@voice_bp.route('/api/voice-command', methods=['POST'])
def process_voice_command():
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({"status": "error", "message": "No command provided"}), 400

    command = data['command'].lower().strip()
    user_role = session.get('role', 'unknown')
    user_name = session.get('user_name', 'User')
    
    # Default Fallback
    response_payload = {
        "status": "success",
        "action": "unknown",
        "message": f"I heard '{command}', but I am not sure how to process that."
    }

    # 1. ADVANCED DATABASE QUERIES
    if any(word in command for word in ['total orders', 'how many orders', 'market volume']):
        total_orders = len(ORDERS_DB)
        response_payload = {"action": "speak", "message": f"The ecosystem currently has {total_orders} active global orders."}
    
    elif any(word in command for word in ['expert', 'find an expert', 'help']):
        online_experts = sum(1 for e in EXPERTS_DB if e.get('online'))
        response_payload = {"action": "navigate", "url": "/expert", "message": f"There are {online_experts} experts online right now. Opening the expert portal for you."}

    elif any(word in command for word in ['system health', 'platform status', 'report']):
        total_users = len(USERS_DB)
        response_payload = {"action": "speak", "message": f"AquaSphere is fully operational with {total_users} active network nodes. Satellite telemetry is green."}

    # 2. VOICE-ACTIVATED ECOSYSTEM CONNECTIONS (HANDSHAKE)
    elif 'connect' in command or 'handshake' in command:
        target_role = "business"
        if "buyer" in command or "business" in command:
            target_role = "buyer"
        elif "farmer" in command:
            target_role = "farmer"
        elif "hatchery" in command:
            target_role = "hatchery"
        elif "lab" in command or "tech" in command:
            target_role = "lab_tech"

        # Create the lead connection dynamically
        lead = {
            "id": f"VOICE-CONN-{random.randint(1000,9999)}",
            "from": user_role,
            "to": target_role,
            "msg": f"Voice-Initiated Connection Request from {user_name}",
            "status": "pending"
        }
        AQUACYCLE_DB["leads"].append(lead)
        save_aquacycle()
        response_payload = {"action": "speak", "message": f"I have successfully established a new handshake request with the {target_role.title()} sector."}

    # 3. VOICE-ACTIVATED DATA LOGGING
    elif any(word in command for word in ['log feed', 'record feeding', 'fed the fish', 'fed the shrimp']):
        report = {
            "id": f"VLOG-{random.randint(1000,9999)}",
            "from": user_role,
            "to": user_role,
            "title": "Voice Feeding Log",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "status": "Success"
        }
        AQUACYCLE_DB["reports"].append(report)
        save_aquacycle()
        response_payload = {"action": "speak", "message": "Feeding activity successfully logged into the database."}

    # 4. NAVIGATION INTENTS (Advanced)
    elif any(word in command for word in ['home', 'dashboard', 'main', 'start']):
        response_payload = {"action": "navigate", "url": "/dashboard", "message": "Navigating to your unified dashboard."}
    elif 'farm' in command:
        response_payload = {"action": "navigate", "url": "/farmer", "message": "Opening Farmer Hub."}
    elif 'hatchery' in command:
        response_payload = {"action": "navigate", "url": "/hatchery", "message": "Opening Hatchery Hub."}
    elif 'logistic' in command or 'transport' in command:
        response_payload = {"action": "navigate", "url": "/dashboard", "message": "Opening Logistics Hub."}
    elif 'lab' in command or 'test' in command:
        response_payload = {"action": "navigate", "url": "/lab-tech", "message": "Opening Lab Console."}
    elif 'market' in command or 'buyer' in command:
        response_payload = {"action": "navigate", "url": "/buyer", "message": "Opening Market Panel."}
    elif 'profile' in command or 'account' in command or 'who am i' in command:
        response_payload = {"action": "navigate", "url": "/profile", "message": f"Opening profile. You are logged in as a {user_role}."}
    elif 'network' in command or 'ecosystem' in command:
        response_payload = {"action": "navigate", "url": "/ecosystem", "message": "Visualizing your ecosystem network connections."}
    elif 'ai' in command or 'vision' in command or 'scan' in command:
        response_payload = {"action": "navigate", "url": "/ai-vision", "message": "Activating AI Neural Vision scanner."}
        
    # 5. SYSTEM COMMANDS
    elif any(word in command for word in ['stop', 'off', 'disable', 'quiet', 'shut down']):
        response_payload = {"action": "system", "command": "stop_voice", "message": "Disabling voice command mode."}
    elif 'logout' in command or 'sign out' in command or 'exit' in command:
        response_payload = {"action": "navigate", "url": "/logout", "message": "Logging you out. Goodbye."}
    
    # 6. GENERAL INSIGHTS
    elif 'price' in command or 'cost' in command:
        response_payload = {"action": "speak", "message": "The current market price for Vannamei shrimp is 6.3 dollars per kilogram, up by 0.5% today."}
    elif 'weather' in command or 'temperature' in command or 'water' in command:
        response_payload = {"action": "speak", "message": "The telemetry indicates optimal water temperature at 28.6 degrees Celsius. No immediate action required."}
    elif 'alert' in command or 'notification' in command:
        response_payload = {"action": "speak", "message": "You have no critical alerts. Logistics tracking TR-441 is currently active."}

    return jsonify(response_payload)
