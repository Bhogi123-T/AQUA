from flask import Blueprint, render_template
from core.auth_utils import role_required, get_trans

logistics_bp = Blueprint('logistics', __name__)

@logistics_bp.route("/logistics")
@role_required(['farmer', 'business', 'transport', 'harvest_contractor', 'processing_plant', 'admin'])
def logistics():
    trans, lang = get_trans()
    return render_template("logistics.html", trans=trans, lang=lang)
