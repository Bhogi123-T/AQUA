from flask import Blueprint, render_template, request, jsonify, session
from core.auth_utils import get_trans, role_required, login_required
from datetime import datetime
import random

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route("/international-compliance")
@login_required
def international_compliance():
    trans, lang = get_trans()
    
    # Mock data for Global Certifications and Traceability
    certifications = [
        {"name": "ASC (Aquaculture Stewardship Council)", "status": "Compliant", "expiry": "2027-12-31", "region": "Global"},
        {"name": "BAP (Best Aquaculture Practices)", "status": "Pending Renewal", "expiry": "2026-06-15", "region": "USA/EU"},
        {"name": "EU FDA Organic Seafood", "status": "Action Required - Antibiotic Check", "expiry": "2026-05-30", "region": "EU"},
    ]
    
    # Traceability export log
    traceability_logs = [
        {"batch": "B-4421", "origin": "Andhra Pradesh, IN", "destination": "Tokyo, JP", "clearance": "Cleared", "timestamp": "2026-05-04 14:00"},
        {"batch": "B-4422", "origin": "Gujarat, IN", "destination": "Rotterdam, EU", "clearance": "Awaiting Lab Results", "timestamp": "2026-05-05 09:30"}
    ]
    
    return render_template(
        "compliance.html", 
        trans=trans, 
        lang=lang,
        certifications=certifications,
        traceability_logs=traceability_logs
    )
