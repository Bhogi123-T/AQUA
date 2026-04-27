from flask import Blueprint, render_template, jsonify, session # type: ignore
from core.auth_utils import role_required, get_trans

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route("/api/farmer/hub")
@role_required(['farmer', 'admin'])
def api_farmer_hub():
    # Import from core.db to avoid missing variables
    from core.db import PROBLEMS_DB 
    
    trans, lang = get_trans()
    user_id = session.get('user')
    user_problems = [p for p in PROBLEMS_DB if p.get('user_id') == user_id]
    return jsonify({
        "status": "success",
        "problems": user_problems,
        "lang": lang
    })

@farmer_bp.route("/farmer")
@role_required(['farmer', 'admin'])
def farmer_hub():
    trans, lang = get_trans()
    res = api_farmer_hub().get_json()
    return render_template("farmer_dashboard.html", trans=trans, lang=lang, problems=res['problems'])

@farmer_bp.route("/farmer/disease")
@role_required(['farmer', 'admin'])
def disease_page():
    trans, lang = get_trans()
    return render_template("disease_analysis.html", trans=trans, lang=lang)

@farmer_bp.route("/farmer/feed")
@role_required(['farmer', 'admin'])
def feed_page():
    trans, lang = get_trans()
    return render_template("feed_calculation.html", trans=trans, lang=lang)

@farmer_bp.route("/farmer/stocking")
@role_required(['farmer', 'admin'])
def stocking_page():
    trans, lang = get_trans()
    return render_template("stocking_advisor.html", trans=trans, lang=lang)

@farmer_bp.route("/farmer/seed")
@role_required(['farmer', 'admin'])
def seed_page():
    trans, lang = get_trans()
    return render_template("seed_checker.html", trans=trans, lang=lang)

@farmer_bp.route("/farmer/yield")
@role_required(['farmer', 'admin'])
def yield_page():
    trans, lang = get_trans()
    return render_template("yield_forecast.html", trans=trans, lang=lang)
