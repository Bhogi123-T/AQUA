from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

processing_bp = Blueprint('processing', __name__)

@processing_bp.route("/processing-plant")
@role_required(['processing_plant', 'admin'])
def processing_dashboard():
    trans, lang = get_trans()
    return render_template("processing_dashboard.html", trans=trans, lang=lang)
