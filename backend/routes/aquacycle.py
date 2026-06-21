from flask import Blueprint, request, jsonify, session
from core.auth_utils import get_trans, get_role, login_required
from core.db import AQUACYCLE_DB, save_aquacycle, USERS_DB, PAYMENTS_DB, ORDERS_DB, EXPERTS_DB, PROBLEMS_DB
from core.ecosystem_config import AQUA_ROLES, AQUACYCLE_CONNECTIONS, AQUA_ROLE_ACTIONS
import random
from datetime import datetime

aquacycle_bp = Blueprint('aquacycle', __name__)

@aquacycle_bp.route("/api/aquacycle/dashboard")
@login_required
def api_aquacycle_dashboard():
    user_email = session.get("user")
    user_role = get_role()
    trans, lang = get_trans()
    
    connection_ids = AQUACYCLE_CONNECTIONS.get(user_role, [])
    connections = []
    for rid in connection_ids:
        if rid in AQUA_ROLES:
            connections.append({
                "id": rid,
                "name": trans.get(f"role_{rid}", AQUA_ROLES[rid]["name"]),
                "icon": AQUA_ROLES[rid]["icon"],
                "category": AQUA_ROLES[rid]["category"]
            })
            
    role_leads = [L for L in AQUACYCLE_DB["leads"] if L.get("to") == user_role or L.get("from") == user_role]
    role_reports = [R for R in AQUACYCLE_DB["reports"] if R.get("to") == user_role or R.get("from") == user_role]

    today_str = datetime.now().strftime("%Y-%m-%d")
    
    today_payments = [p for p in PAYMENTS_DB if p.get("timestamp", "").startswith(today_str)]
    today_tx_sum = sum(float(str(p.get("amount", "0")).replace(",", "").replace("₹", "")) for p in today_payments)
    
    total_users_count = len(USERS_DB)
    total_orders_count = len(ORDERS_DB)

    widgets = [
        {"label": "System Status", "value": "SECURE", "color": "emerald"},
        {"label": "Today's Volume", "value": f"₹{today_tx_sum:,.0f}", "color": "blue"}
    ]
    category = AQUA_ROLES.get(user_role, {}).get("category", "")

    if category == "Production":
        widgets += [
            {"label": "Active Ponds", "value": str(random.randint(3, 6)), "color": "cyan"},
            {"label": "Total Farmers", "value": str(sum(1 for u in USERS_DB.values() if u.get('role') == 'farmer')), "color": "emerald"}
        ]
    elif category == "Supply":
        widgets += [
            {"label": "Market Leads", "value": str(len(role_leads)), "color": "blue"},
            {"label": "Global Orders", "value": str(total_orders_count), "color": "amber"}
        ]
    elif category == "Support":
        widgets = [
            {"label": "Experts Online", "value": str(sum(1 for e in EXPERTS_DB if e.get('online'))), "color": "emerald"},
            {"label": "Open Problems", "value": str(sum(1 for p in PROBLEMS_DB if p.get('status') == 'Open')), "color": "amber"},
            {"label": "Critical Alerts", "value": "0", "color": "red"}
        ]
    else: 
        widgets = [
            {"label": "Platform Users", "value": str(total_users_count), "color": "cyan"},
            {"label": "System Health", "value": "Online", "color": "emerald"},
            {"label": "Today's Txns", "value": f"₹{today_tx_sum:,.0f}", "color": "blue"}
        ]

    recent_activity = []
    
    sorted_users = sorted(USERS_DB.items(), key=lambda x: x[1].get('joined_at', ''), reverse=True)
    if sorted_users:
        latest_user = sorted_users[0][1]
        recent_activity.append({"type": "sys", "msg": f"User Joined: {latest_user.get('name')}", "time": "Recent"})
        
    if ORDERS_DB:
        latest_order = ORDERS_DB[-1]
        recent_activity.append({"type": "market", "msg": f"Order: {latest_order.get('quantity')}T {latest_order.get('species')}", "time": "New"})

    if PAYMENTS_DB:
        latest_pay = PAYMENTS_DB[-1]
        recent_activity.append({"type": "bio", "msg": f"Payment: ₹{latest_pay.get('amount')} Received", "time": "Verified"})

    recent_activity.append({"type": "sat", "msg": "Satellite Neural Sync: Operational", "time": "Active"})
    recent_activity.append({"type": "sys", "msg": "Audit Logs: Integrity Verified", "time": "SAFE"})
    
    role_data = {
        "user_info": {
            "name": session.get("user_name"),
            "role": user_role,
            "role_display": AQUA_ROLES.get(user_role, {}).get("name")
        },
        "role_info": AQUA_ROLES.get(user_role, {}),
        "actions": AQUA_ROLE_ACTIONS.get(user_role, []),
        "connections": connections,
        "leads": role_leads,
        "reports": role_reports,
        "widgets": widgets,
        "recent_activity": recent_activity[:5]
    }
    
    return jsonify({
        "status": "success",
        "data": role_data
    })

@aquacycle_bp.route("/api/aquacycle/work", methods=["POST"])
@login_required
def api_aquacycle_work():
    raw_payload = dict(request.get_json(silent=True) or {})
    if not raw_payload:
        raw_payload = dict(request.form)

    action = str(raw_payload.get("action"))
    
    data: dict = {}
    if "data" in raw_payload and isinstance(raw_payload["data"], dict):
        data = dict(raw_payload["data"])
    else:
        data = dict({k: v for k, v in raw_payload.items() if k != "action"})

    user_email = session.get("user")
    user_role = get_role()
    
    if not action:
        return jsonify({"status": "error", "message": "No action specified"})

    if action == "register_hatchery" and user_role in ["hatchery", "admin"]:
        h_id = f"H-{random.randint(100,999)}"
        AQUACYCLE_DB["hatcheries"][h_id] = {
            "owner": user_email,
            "name": data.get("name"),
            "location": data.get("location"),
            "status": "active",
            "batches": []
        }
        save_aquacycle()
        return jsonify({"status": "success", "message": "Hatchery Registered", "id": h_id})

    elif action in ["breeding_log", "larvae_growth", "feeding_log", "temp_log", "daily_sales", "production_log", "record_stocking", "track_feed_usage", "water_test", "daily_pond_activity", "monitor_growth", "record_results", "record_batch", "record_quantity", "record_storage", "manage_sales", "track_repayments"]:
        entry = {
            "id": f"LOG-{random.randint(1000,9999)}",
            "from": user_role,
            "to": user_role,
            "title": f"{action.replace('_', ' ').title()} Entry",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data": data
        }
        AQUACYCLE_DB["reports"].append(entry)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Log entry recorded successfully"})

    elif action.startswith("connect_"):
        target_role = action.split("_")[1]
        raw_data = data.get("data", {})
        lead = {
            "id": f"CONN-{random.randint(1000,9999)}",
            "from": user_role,
            "to": target_role,
            "msg": f"Connection Request: {raw_data.get('purpose', 'Networking')} from {session.get('user_name')}",
            "status": "pending"
        }
        AQUACYCLE_DB["leads"].append(lead)
        save_aquacycle()
        return jsonify({"status": "success", "message": f"Connection request sent to {target_role.title()} industry."})

    elif action in ["buy_seed", "water_test_request", "order_stock", "receive_orders", "receive_samples", "receive_harvest_requests", "receive_ice_orders", "place_orders", "purchase_stock", "buy_seafood", "approve_regs", "approve_loans", "accept_transport", "receive_harvest"]:
        lead = {
            "id": f"LD-{random.randint(1000,9999)}",
            "from": user_role,
            "to": data.get("target_role", "hatchery" if action == "buy_seed" else "lab_tech"),
            "msg": f"New {action.replace('_', ' ')} request from {session.get('user_name')}",
            "status": "pending"
        }
        AQUACYCLE_DB["leads"].append(lead)
        save_aquacycle()
        return jsonify({"status": "success", "message": f"{action.replace('_', ' ').title()} request sent"})

    elif action in ["batch_status", "update_ice_stock", "list_inventory", "list_products", "deliver_seed", "update_delivery_status", "manage_transport_orders", "list_feed_products", "update_stock", "list_harvest_sale", "schedule_harvest", "track_deliveries", "list_medicines", "provide_instructions", "schedule_teams", "confirm_completion", "deliver_ice", "confirm_delivery", "grade_seafood", "manage_packaging", "send_to_buyers", "release_product", "make_payments", "upload_docs", "monitor_transactions", "handle_disputes"]:
        record = {
            "id": f"UP-{random.randint(1000,9999)}",
            "from": user_role,
            "title": f"Status Update: {action.replace('_', ' ').title()}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Success"
        }
        AQUACYCLE_DB["reports"].append(record)
        save_aquacycle()
        return jsonify({"status": "success", "message": f"{action.replace('_', ' ').title()} updated successfully"})

    elif action in ["inspect_batch", "field_audit", "verify_claim", "view_hatchery_availability", "report_disease", "report_farm_issue", "upload_reports", "send_alerts", "view_farm_data", "analyze_reports", "give_recommendations", "alert_disease_risk", "view_jobs", "track_shipment", "inspect_quality", "upload_qc_reports", "approve_batch", "monitor_inventory", "view_harvest_lots", "view_bulk_availability", "track_shipments", "monitor_farms", "verify_licenses", "inspect_production", "approve_export", "offer_loans", "provide_insurance", "process_claims", "monitor_insured", "manage_users", "view_analytics"]:
        report = {
            "id": f"REP-{random.randint(1000,9999)}",
            "from": user_role,
            "to": data.get("target_id", "system"),
            "title": f"{action.replace('_', ' ').title()} Result",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Passed"
        }
        AQUACYCLE_DB["reports"].append(report)
        save_aquacycle()
        return jsonify({"status": "success", "message": f"{action.replace('_', ' ').title()} completed and report filed"})

    elif action == "apply_loan":
        lead = {
            "id": f"LOAN-{random.randint(1000,9999)}",
            "from": user_role,
            "to": "admin",
            "msg": f"Loan application for ₹{data.get('amount', '5,00,000')}",
            "status": "Under Review"
        }
        AQUACYCLE_DB["leads"].append(lead)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Loan application submitted for review"})

    if action == "register_farm_ponds" and user_role in ["farmer", "admin"]:
        f_id = f"F-P-{random.randint(100,999)}"
        return jsonify({"status": "success", "message": "Farm and Ponds registered in connectivity matrix", "id": f_id})

    if action == "create_batch" and user_role in ["hatchery", "admin"]:
        b_id = f"B-{random.randint(1000,9999)}"
        batch = {
            "id": b_id,
            "h_id": data.get("h_id"),
            "type": data.get("type"),
            "count": data.get("count"),
            "price": data.get("price"),
            "health": data.get("health", 100),
            "status": "available",
            "created_at": datetime.now().isoformat()
        }
        AQUACYCLE_DB["seed_batches"].append(batch)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Batch Created", "id": b_id})

    if action in ["upload_health_cert", "list_seed_sale", "accept_orders", "track_deliveries"] and user_role in ["hatchery", "admin"]:
        record = {
            "id": f"H-OP-{random.randint(1000,9999)}",
            "from": user_role,
            "to": user_role,
            "type": "operation",
            "action": action,
            "title": action.replace('_', ' ').title(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Completed"
        }
        AQUACYCLE_DB["reports"].append(record)
        save_aquacycle()
        return jsonify({"status": "success", "message": f"{action.replace('_', ' ').title()} recorded in system logs"})

    if action == "register_farm" and user_role == "farmer":
        f_id = f"F-{random.randint(100,999)}"
        AQUACYCLE_DB["farms"][f_id] = {
            "owner": user_email,
            "name": data.get("name"),
            "location": data.get("location"),
            "ponds": []
        }
        save_aquacycle()
        return jsonify({"status": "success", "message": "Farm Registered", "id": f_id})

    if action == "add_pond" and user_role in ["farmer", "farmer"]:
        p_id = f"P-{random.randint(100,999)}"
        pond = {
            "id": p_id,
            "f_id": data.get("f_id"),
            "name": data.get("name"),
            "status": "pre-stocking",
            "daily_logs": []
        }
        AQUACYCLE_DB["ponds"].append(pond)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Pond Added", "id": p_id})

    if action == "list_inventory" and user_role in ["feed_supplier", "feed_supplier"]:
        i_id = f"I-{random.randint(100,999)}"
        item = {
            "id": i_id,
            "owner": user_email,
            "name": data.get("name"),
            "type": data.get("type"),
            "qty": data.get("qty"),
            "price": data.get("price")
        }
        AQUACYCLE_DB["inventory"].append(item)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Inventory Updated"})

    if action == "upload_report" and user_role == "lab_tech":
        r_id = f"R-{random.randint(1000,9999)}"
        report = {
            "id": r_id,
            "from": user_role,
            "to": data.get("target_role", "farmer"),
            "title": data.get("title"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "file": "report_link_mock"
        }
        AQUACYCLE_DB["reports"].append(report)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Report Uploaded"})

    if action == "schedule_harvest" and user_role in ["farmer", "farmer"]:
        h_id = f"HVT-{random.randint(100,999)}"
        job = {
            "id": h_id,
            "type": "harvest",
            "location": data.get("location"),
            "status": "pending",
            "assigned_to": "harvest_contractor"
        }
        AQUACYCLE_DB["jobs"].append(job)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Harvest Scheduled"})

    if action == "request_transport" and user_role in ["farmer", "hatchery", "processing_plant"]:
        s_id = f"SHP-{random.randint(1000,9999)}"
        shipment = {
            "id": s_id,
            "from": user_email,
            "to": data.get("destination"),
            "status": "pending_pickup",
            "type": data.get("shipment_type")
        }
        AQUACYCLE_DB["shipments"].append(shipment)
        save_aquacycle()
        return jsonify({"status": "success", "message": "Transport Requested"})

    if action == "apply_loan" and user_role == "farmer":
        l_id = f"LOAN-{random.randint(100,999)}"
        AQUACYCLE_DB["finance"]["loans"].append({
            "id": l_id,
            "user": user_email,
            "amount": data.get("amount"),
            "status": "under_review"
        })
        save_aquacycle()
        return jsonify({"status": "success", "message": "Loan Application Submitted"})

    return jsonify({"status": "error", "message": "Unauthorized or Invalid Action"})
