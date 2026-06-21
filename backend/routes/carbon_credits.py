from flask import Blueprint, render_template, request, jsonify, session
from core.auth_utils import get_trans, role_required, login_required

carbon_credits_bp = Blueprint('carbon_credits', __name__)

@carbon_credits_bp.route("/esg-carbon-credits")
@login_required
def carbon_credits():
    trans, lang = get_trans()
    
    # Mock data for ESG and Carbon Trading
    esg_score = 87
    total_carbon_offset = "450 Tons CO2e"
    
    from ml_core.models_loader import get_global_prices
    
    eu_prices = get_global_prices(49.00) # €45 ~ $49
    jp_prices = get_global_prices(45.00) # ¥6800 ~ $45
    us_prices = get_global_prices(52.00) # $52
    
    def m_curr(p):
        return f"${p['USD']} / €{p['EUR']} / ₹{p['INR']} / ¥{p['JPY']}"
    
    credit_market = [
        {"buyer": "EU Eco Fund", "volume_required": "1000 Tons", "price_per_ton": m_curr(eu_prices), "status": "Open"},
        {"buyer": "Japan Blue Ocean Init.", "volume_required": "500 Tons", "price_per_ton": m_curr(jp_prices), "status": "Negotiating"},
        {"buyer": "US SustainAqua", "volume_required": "2000 Tons", "price_per_ton": m_curr(us_prices), "status": "Open"}
    ]
    
    sustainable_practices = [
        {"practice": "Solar Aeration Transition", "impact": "-120 Tons CO2/yr", "verified": True},
        {"practice": "Mangrove Reforestation Buffer", "impact": "-300 Tons CO2/yr", "verified": True},
        {"practice": "Zero-Water Exchange System", "impact": "Water footprint reduced by 80%", "verified": False}
    ]
    
    return render_template(
        "carbon_credits.html", 
        trans=trans, 
        lang=lang,
        esg_score=esg_score,
        total_carbon_offset=total_carbon_offset,
        credit_market=credit_market,
        sustainable_practices=sustainable_practices
    )

@carbon_credits_bp.route("/api/sustainability-score", methods=["GET"])
@login_required
def api_sustainability_score():
    import random
    score = random.randint(70, 98)
    
    # Calculate ESG badge based on score
    if score > 90:
        badge = "Platinum ESG Certified"
        eu_eligible = True
    elif score > 80:
        badge = "Gold ESG Certified"
        eu_eligible = True
    else:
        badge = "Silver ESG Participant"
        eu_eligible = False
        
    return jsonify({
        "status": "success",
        "farmer_id": session.get('user'),
        "esg_score": score,
        "badge": badge,
        "eu_export_eligible": eu_eligible,
        "metrics": {
            "feed_efficiency": f"{random.uniform(1.1, 1.8):.2f} FCR",
            "chemical_usage": "Zero Antibiotics Verified",
            "water_quality": "95% Optimal Uptime",
            "yield_to_loss": f"{random.randint(85, 95)}% Survival"
        },
        "message": "ESG Certification automatically generated."
    })
