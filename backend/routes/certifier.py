from flask import Blueprint, render_template, request, jsonify
from core.auth_utils import role_required, get_trans
from core.db import AQUACYCLE_DB, save_aquacycle
import random

certifier_bp = Blueprint('certifier', __name__)

def _ensure_mock_certs():
    if "certifications" not in AQUACYCLE_DB:
        AQUACYCLE_DB["certifications"] = []
    if not AQUACYCLE_DB["certifications"]:
        AQUACYCLE_DB["certifications"] = [
            {"id": "CERT-881", "farm": "Blue Water Farms", "type": "Organic Export Ready", "disease_score": "98% Clean", "lab_status": "Passed", "status": "Pending", "date": "2026-06-02"},
            {"id": "CERT-882", "farm": "Coastal Aqua", "type": "Sustainability ISO", "disease_score": "92% Clean", "lab_status": "Passed", "status": "Approved", "date": "2026-05-15"},
            {"id": "CERT-883", "farm": "Mekong Delta Shrimps", "type": "Antibiotic Free", "disease_score": "75% Clean", "lab_status": "Failed - Traces Found", "status": "Pending", "date": "2026-06-06"}
        ]
        save_aquacycle()

@certifier_bp.route("/certifier")
@role_required(['certifier', 'admin'])
def certifier_dashboard():
    trans, lang = get_trans()
    _ensure_mock_certs()
    certs = AQUACYCLE_DB["certifications"]
    
    pending_count = sum(1 for c in certs if c["status"] == "Pending")
    approved_count = sum(1 for c in certs if c["status"] == "Approved")
    
    return render_template("certifier_dashboard.html", trans=trans, lang=lang, certs=certs, stats={
        "pending": pending_count,
        "approved": approved_count,
        "total": len(certs)
    })

@certifier_bp.route("/certifier/action", methods=["POST"])
@role_required(['certifier', 'admin'])
def cert_action():
    data = request.get_json()
    cert_id = data.get("cert_id")
    action = data.get("action")
    
    for cert in AQUACYCLE_DB["certifications"]:
        if cert["id"] == cert_id:
            cert["status"] = "Approved" if action == "approve" else "Rejected"
            save_aquacycle()
            return jsonify({"status": "success", "new_status": cert["status"]})
            
    return jsonify({"status": "error", "message": "Certification request not found"}), 404
