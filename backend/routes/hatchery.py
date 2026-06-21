from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

hatchery_bp = Blueprint('hatchery', __name__)

@hatchery_bp.route("/hatchery")
@role_required(['hatchery', 'admin'])
def hatchery_dashboard():
    trans, lang = get_trans()
    return render_template("hatchery_dashboard.html", trans=trans, lang=lang)
