from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

exporter_bp = Blueprint('exporter', __name__)

@exporter_bp.route("/exporter")
@role_required(['exporter', 'admin'])
def exporter_dashboard():
    trans, lang = get_trans()
    return render_template("exporter_dashboard.html", trans=trans, lang=lang)
