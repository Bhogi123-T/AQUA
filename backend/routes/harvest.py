from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

harvest_bp = Blueprint('harvest', __name__)

@harvest_bp.route("/harvest-contractor")
@role_required(['harvest_contractor', 'admin'])
def harvest_dashboard():
    trans, lang = get_trans()
    return render_template("harvest_dashboard.html", trans=trans, lang=lang)
