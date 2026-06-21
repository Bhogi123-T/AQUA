from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

cold_storage_bp = Blueprint('cold_storage', __name__)

@cold_storage_bp.route("/cold-storage")
@role_required(['cold_storage', 'admin'])
def cold_storage_dashboard():
    trans, lang = get_trans()
    return render_template("cold_storage_dashboard.html", trans=trans, lang=lang)
