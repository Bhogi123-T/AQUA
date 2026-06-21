from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

broodstock_bp = Blueprint('broodstock', __name__)

@broodstock_bp.route("/broodstock")
@role_required(['broodstock', 'admin'])
def broodstock_dashboard():
    trans, lang = get_trans()
    return render_template("broodstock_dashboard.html", trans=trans, lang=lang)
