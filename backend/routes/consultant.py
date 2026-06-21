from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

consultant_bp = Blueprint('consultant', __name__)

@consultant_bp.route("/consultant")
@role_required(['consultant', 'admin'])
def consultant_dashboard():
    trans, lang = get_trans()
    return render_template("consultant_dashboard.html", trans=trans, lang=lang)
