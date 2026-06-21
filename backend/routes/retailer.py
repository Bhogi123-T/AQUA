from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

retailer_bp = Blueprint('retailer', __name__)

@retailer_bp.route("/retailer")
@role_required(['retailer', 'admin'])
def retailer_dashboard():
    trans, lang = get_trans()
    return render_template("retailer_dashboard.html", trans=trans, lang=lang)
