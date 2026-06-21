from flask import Blueprint, render_template, request, jsonify, session
from core.auth_utils import get_trans, role_required, login_required
from datetime import datetime
import random

global_intel_bp = Blueprint('global_intel', __name__)

@global_intel_bp.route("/global-intel")
@login_required
def global_intelligence():
    trans, lang = get_trans()
    
    # Mock data for Global Market Arbitrage and Marine Intelligence
    marine_data = {
        "ocean_currents": "El Niño active - Expect higher temperatures in APAC region.",
        "global_weather": "Storm warnings in South China Sea, stable conditions in Indian Ocean.",
        "marine_ph_shifts": "Slight acidification in Bay of Bengal (-0.1 pH).",
    }
    
    from ml_core.models_loader import get_global_prices
    
    # Generate dynamic arbitrage data using the global currency exchange rates
    shrimp_prices = get_global_prices(6.20)
    tilapia_prices = get_global_prices(1.80)
    crab_prices = get_global_prices(15.00)
    
    arbitrage_data = [
        {
            "species": "Vannamei Shrimp", 
            "local_price": f"₹{shrimp_prices['INR']}/kg", 
            "global_price": f"${shrimp_prices['USD']} / €{shrimp_prices['EUR']} / ₫{shrimp_prices['VND']} / ฿{shrimp_prices['THB']}", 
            "demand": "High in EU", "trend": "UP (+2.5%)"
        },
        {
            "species": "Tilapia", 
            "local_price": f"₹{tilapia_prices['INR']}/kg", 
            "global_price": f"${tilapia_prices['USD']} / €{tilapia_prices['EUR']} / ₫{tilapia_prices['VND']} / ฿{tilapia_prices['THB']}", 
            "demand": "Stable in USA", "trend": "FLAT"
        },
        {
            "species": "Mud Crab", 
            "local_price": f"₹{crab_prices['INR']}/kg", 
            "global_price": f"${crab_prices['USD']} / ¥{crab_prices['JPY']} / ₫{crab_prices['VND']} / ฿{crab_prices['THB']}", 
            "demand": "Surging in Japan", "trend": "UP (+8.1%)"
        }
    ]
    
    currency_rates = {
        "USD": 83.0,
        "EUR": 90.5,
        "JPY": 0.55
    }
    
    return render_template(
        "global_intel.html", 
        trans=trans, 
        lang=lang,
        marine_data=marine_data,
        arbitrage_data=arbitrage_data,
        currency_rates=currency_rates
    )

@global_intel_bp.route("/api/global/heatmap", methods=["GET"])
@role_required(['admin', 'regulator', 'bank', 'expert'])
def api_disease_heatmap():
    from core.knowledge_base import GLOBAL_AQUA_REGIONS
    
    # Generate mock heatmap data for regions based on water quality and disease reports
    # This fulfills the ideation concept: "Selling regional disease heatmaps to government/insurance"
    heatmap_data = []
    
    regions = ["Andhra Pradesh", "Gujarat", "West Bengal", "Tamil Nadu", "Odisha"]
    for region in regions:
        risk_level = random.choice(["Low", "Moderate", "High", "Critical"])
        disease = "None"
        if risk_level in ["High", "Critical"]:
            disease = random.choice(["WSSV (White Spot)", "EHP", "Vibrio", "EMS"])
            
        heatmap_data.append({
            "region": region,
            "coordinates": {
                "lat": random.uniform(13.0, 22.0),
                "lng": random.uniform(70.0, 88.0)
            },
            "risk_level": risk_level,
            "active_threat": disease,
            "affected_farms": random.randint(0, 50) if risk_level != "Low" else 0,
            "data_value_usd": random.randint(1000, 5000) # Market value of this intel
        })
        
    return jsonify({
        "status": "success",
        "message": "Aggregated Regional Disease Heatmap Data",
        "data_monetization_ready": True,
        "heatmap": heatmap_data
    })
