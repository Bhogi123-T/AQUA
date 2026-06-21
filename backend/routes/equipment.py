from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route("/equipment")
@role_required(['equipment', 'admin'])
def equipment_dashboard():
    trans, lang = get_trans()
    return render_template("equipment_dashboard.html", trans=trans, lang=lang)
