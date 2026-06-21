from flask import Blueprint, render_template, request, jsonify
from core.auth_utils import role_required, get_trans
from core.db import AQUACYCLE_DB, save_aquacycle
import random

bank_bp = Blueprint('bank', __name__)

def _ensure_mock_loans():
    if "finance" not in AQUACYCLE_DB:
        AQUACYCLE_DB["finance"] = {"loans": [], "insurance": []}
    if not AQUACYCLE_DB["finance"].get("loans"):
        AQUACYCLE_DB["finance"]["loans"] = [
            {"id": "LN-1001", "farmer": "Ravi Kumar", "amount": 500000, "purpose": "Pond expansion & aerators", "ai_risk_score": "Low Risk", "yield_pred": "4.2 Tons", "status": "Pending", "date": "2026-06-01"},
            {"id": "LN-1002", "farmer": "Sita Ram", "amount": 1200000, "purpose": "New Vannamei seed batch", "ai_risk_score": "High Risk", "yield_pred": "1.8 Tons", "status": "Pending", "date": "2026-06-05"},
            {"id": "LN-1003", "farmer": "Chen Chen", "amount": 350000, "purpose": "Solar power installation", "ai_risk_score": "Medium Risk", "yield_pred": "3.5 Tons", "status": "Approved", "date": "2026-05-28"}
        ]
        save_aquacycle()

@bank_bp.route("/bank")
@role_required(['bank', 'admin'])
def bank_dashboard():
    trans, lang = get_trans()
    _ensure_mock_loans()
    loans = AQUACYCLE_DB["finance"]["loans"]
    
    pending_count = sum(1 for l in loans if l["status"] == "Pending")
    approved_count = sum(1 for l in loans if l["status"] == "Approved")
    total_requested = sum(l["amount"] for l in loans)
    
    return render_template("bank_dashboard.html", trans=trans, lang=lang, loans=loans, stats={
        "pending": pending_count,
        "approved": approved_count,
        "total": total_requested
    })

@bank_bp.route("/bank/loan/action", methods=["POST"])
@role_required(['bank', 'admin'])
def loan_action():
    data = request.get_json()
    loan_id = data.get("loan_id")
    action = data.get("action")
    
    for loan in AQUACYCLE_DB["finance"]["loans"]:
        if loan["id"] == loan_id:
            loan["status"] = "Approved" if action == "approve" else "Rejected"
            save_aquacycle()
            return jsonify({"status": "success", "new_status": loan["status"]})
            
    return jsonify({"status": "error", "message": "Loan not found"}), 404
