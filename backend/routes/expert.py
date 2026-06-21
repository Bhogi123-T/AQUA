from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from core.auth_utils import login_required, get_trans, role_required
from core.db import EXPERTS_DB, SESSIONS_DB, PROBLEMS_DB, save_problems, COMMUNITY_DB, USERS_DB
from werkzeug.utils import secure_filename
import os
import time
from datetime import datetime

expert_bp = Blueprint('expert', __name__)

# Note: Ideally, this config parameter should be passed differently to avoid circular import
# with `app`. For this extraction, we'll assume `UPLOAD_FOLDER` is 'static/uploads'
UPLOAD_FOLDER = 'static/uploads'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expert_bp.route("/expert/dashboard")
@role_required(['expert', 'admin'])
def expert_dashboard():
    trans, lang = get_trans()
    user_id = session.get('user')
    user_role = USERS_DB.get(user_id, {}).get('role', 'expert')

    expert_data = next((e for e in EXPERTS_DB if e.get('user_id') == user_id), None) or (EXPERTS_DB[0] if EXPERTS_DB else {})

    if user_role == 'admin':
        my_sessions = SESSIONS_DB
    else:
        my_sessions = [s for s in SESSIONS_DB if s.get('expert_id') == user_id or s.get('user_id') == user_id]

    knowledge_articles = [
        {"icon": "🦐", "title": "Advanced Vannamei Management", "desc": "Comprehensive guide.", "author": "Dr. A. Sharma", "views": "2.4K"},
        {"icon": "💊", "title": "Disease Prevention Protocol", "desc": "Step-by-step WSSV prevention.", "author": "Dr. Chen Wei", "views": "1.8K"},
    ]
    posts = list(reversed(COMMUNITY_DB.get("posts", [])))[:10] if "posts" in COMMUNITY_DB else []
    groups = ["Vannamei Growers", "Water Quality Telugu", "Disease Alerts AP", "Organic Prawn Trade"]

    # We mock analytics since get_community_analytics was in app.py and not extracted
    analytics = {"total_posts": len(posts), "active_users": 150}

    return render_template("expert_portal.html",
                           trans=trans, lang=lang,
                           experts=EXPERTS_DB,
                           user_is_expert=(user_role in ['expert', 'admin']),
                           active_sessions=sum(1 for e in EXPERTS_DB if e.get('online')),
                           my_sessions=my_sessions,
                           posts=posts, groups=groups, analytics=analytics,
                           knowledge_articles=knowledge_articles,
                           expert_data=expert_data,
                           active_tab='dashboard')

@expert_bp.route("/support")
def support_center():
    trans, lang = get_trans()
    return render_template("knowledge_hub.html", trans=trans, lang=lang)

@expert_bp.route("/api/export-compliance", methods=["POST"])
def export_compliance_api():
    trans, lang = get_trans()
    data = request.get_json()
    import random
    batch_id = f"AQ-{random.randint(1000, 9999)}"
    return jsonify({
        "status": "APPROVED",
        "batch_id": batch_id,
        "region": data.get('region', 'EU'),
        "expiry": (datetime.now().year + 1),
        "certified_by": "AquaSphere neural-validator"
    })

@expert_bp.route("/farmer/report-problem", methods=["POST"])
@role_required(['farmer', 'admin'])
def report_problem():
    user_id = session.get('user')
    title = request.form.get("title", "Health Alert")
    description = request.form.get("description", "")
    species = request.form.get("species", "Vannamei")
    
    media_url = ""
    if 'media' in request.files:
        file = request.files['media']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"prob_{int(time.time())}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(file_path)
            media_url = f"/static/uploads/{filename}"

    problem = {
        "id": f"PRB-{len(PROBLEMS_DB)+101}",
        "user_id": user_id,
        "user_name": session.get('user_name', 'Farmer'),
        "title": title,
        "description": description,
        "species": species,
        "media_url": media_url,
        "status": "Open",
        "expert_id": None,
        "expert_name": None,
        "solution": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    PROBLEMS_DB.append(problem)
    save_problems()
    
    flash("Problem reported successfully! Experts have been notified.", "success")
    _, lang = get_trans()
    return redirect(url_for("farmer.farmer_hub", lang=lang))

@expert_bp.route("/expert/resolve-problem", methods=["POST"])
@role_required(['expert', 'admin'])
def resolve_problem():
    expert_id = session.get('user')
    expert_name = session.get('user_name', 'Expert')
    prob_id = request.form.get("problem_id")
    solution = request.form.get("solution", "")
    
    for prob in PROBLEMS_DB:
        if prob["id"] == prob_id:
            prob["status"] = "Resolved"
            prob["expert_id"] = expert_id
            prob["expert_name"] = expert_name
            prob["solution"] = solution
            prob["resolved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
            
    save_problems()
    
    flash("Solution submitted! The farmer will be notified.", "success")
    _, lang = get_trans()
    return redirect(url_for("expert.expert_dashboard", lang=lang))

@expert_bp.route("/api/problems")
@login_required
def api_get_problems():
    user_id = session.get('user')
    role = session.get('role')
    
    if role == 'admin':
        return jsonify(PROBLEMS_DB)
    elif role == 'expert':
        return jsonify([p for p in PROBLEMS_DB if p["status"] == "Open" or p["expert_id"] == user_id])
    else:
        return jsonify([p for p in PROBLEMS_DB if p["user_id"] == user_id])

@expert_bp.route("/ai-intelligence")
@role_required(['farmer', 'business', 'expert', 'admin'])
def ai_intelligence_hub():
    trans, lang = get_trans()
    return render_template("ai_engine.html", trans=trans, lang=lang)
