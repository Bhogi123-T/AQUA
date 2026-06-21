from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

lab_tech_bp = Blueprint('lab_tech', __name__)

@lab_tech_bp.route("/lab-tech")
@role_required(['lab_tech', 'admin'])
def lab_tech_dashboard():
    trans, lang = get_trans()
    return render_template("technician_dashboard.html", trans=trans, lang=lang)
