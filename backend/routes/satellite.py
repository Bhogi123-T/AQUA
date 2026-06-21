from flask import Blueprint, render_template, request, jsonify, session
from core.auth_utils import get_trans, role_required, login_required
import random

satellite_bp = Blueprint('satellite', __name__)

@satellite_bp.route("/satellite-mapping")
@login_required
def satellite_mapping():
    trans, lang = get_trans()
    
    # Mock data for satellite telemetry
    satellite_feeds = [
        {"zone": "Zone Alpha (Vietnam)", "status": "Active", "water_turbidity": "High", "algae_bloom_risk": "Critical ⚠️", "last_sync": "2 mins ago"},
        {"zone": "Zone Beta (India - AP)", "status": "Active", "water_turbidity": "Normal", "algae_bloom_risk": "Low ✅", "last_sync": "5 mins ago"},
        {"zone": "Zone Gamma (Ecuador)", "status": "Cloud Cover", "water_turbidity": "Unknown", "algae_bloom_risk": "Unknown", "last_sync": "1 hour ago"},
    ]
    
    geo_stats = {
        "active_satellites": 4,
        "total_area_scanned": "1.2M Hectares",
        "threats_detected": 12
    }
    
    return render_template(
        "satellite.html", 
        trans=trans, 
        lang=lang,
        satellite_feeds=satellite_feeds,
        geo_stats=geo_stats
    )
