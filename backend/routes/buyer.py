from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from core.auth_utils import role_required, login_required, get_trans
import random
from datetime import datetime
from ml_core.models_loader import USD_TO_INR

buyer_bp = Blueprint('buyer', __name__)

USD_TO_INR = 83.0

@buyer_bp.route("/buyer")
@role_required(['buyer', 'admin'])
def buyer_dashboard_route():
    trans, lang = get_trans()
    return render_template("buyer_dashboard.html", trans=trans, lang=lang)

@buyer_bp.route("/api/market")
def api_market_data():
    trans, lang = get_trans()
    base_stocks = [
        {"id": 1, "country": "Norway", "state": "Nordland", "species": "Salmon", "qty": 45, "price": 12.5, "flag": "🇳🇴"},
        {"id": 2, "country": "Vietnam", "state": "Mekong Delta", "species": "Vannamei", "qty": 120, "price": 6.8, "flag": "🇻🇳"},
        {"id": 3, "country": "India", "state": "Andhra Pradesh", "species": "Tiger Prawn", "qty": 85, "price": 8.2, "flag": "🇮🇳"},
        {"id": 4, "country": "USA", "state": "Gulf Coast", "species": "Catfish", "qty": 200, "price": 4.5, "flag": "🇺🇸"},
        {"id": 5, "country": "Brazil", "state": "Northeast", "species": "Tilapia", "qty": 300, "price": 3.2, "flag": "🇧🇷"},
        {"id": 6, "country": "China", "state": "Guangdong", "species": "Mud Crab", "qty": 50, "price": 22.0, "flag": "🇨🇳"},
        {"id": 7, "country": "Bangladesh", "state": "Khulna", "species": "Rohu", "qty": 150, "price": 2.5, "flag": "🇧🇩"},
        {"id": 8, "country": "Thailand", "state": "Eastern Gulf", "species": "Seabass", "qty": 60, "price": 10.5, "flag": "🇹🇭"}
    ]
    
    stocks = []
    for s in base_stocks:
        fluctuation = 1 + (random.uniform(-0.02, 0.02))
        s['price'] = round(s['price'] * fluctuation, 2)
        s['price_inr'] = round(s['price'] * USD_TO_INR, 2)
        s['last_update'] = datetime.now().strftime("%H:%M:%S")
        s['species_display'] = trans.get(f"species_{s['species'].lower().replace(' ', '_')}", s['species'])
        s['country_display'] = trans.get(f"country_{s['country'].lower().replace(' ', '_')}", s['country'])
        s['state_display'] = trans.get(f"region_{s['state'].lower().replace(' ', '_')}", s['state'])
        stocks.append(s)

    return jsonify({"status": "success", "stocks": stocks})

@buyer_bp.route("/market")
def market():
    res = api_market_data().get_json()
    trans, lang = get_trans()
    return render_template("market.html", trans=trans, lang=lang, stocks=res['stocks'])

@buyer_bp.route("/place_order", methods=["GET", "POST"])
@login_required
def place_order():
    if request.method == "GET":
        return redirect(url_for('main.dashboard', lang=request.args.get('lang', 'en')))
    trans, lang = get_trans()
    species = request.form.get("species")
    country = request.form.get("country")
    qty = request.form.get("qty")
    
    # Live Tracking: Origin -> Destination
    origin = f"{country} Central Hub"
    destination = session.get("user", "Guest Portal")
    
    msg = trans['order_msg'].format(qty=qty, species=species, country=country)
    tracking_info = f"Transport Path: {origin} 🚛 → {destination} (Live Tracking Active)"
    
    return render_template("result.html", trans=trans, lang=lang,
                         title=trans['order_success'],
                         description=msg,
                         result="ORDER PLACED",
                         unit=tracking_info)
