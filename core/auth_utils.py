from flask import session, request, redirect, url_for, flash # type: ignore
from functools import wraps
from core.translations import TRANSLATIONS # type: ignore
from core.ecosystem_config import ROLE_MAP, AQUA_ROLES

def get_trans():
    lang = request.args.get('lang')
    if lang:
        # If user explicitly picked a language via URL
        if lang in TRANSLATIONS:
            session['lang'] = lang
            session['manual_lang'] = True
        elif lang == 'auto':
            lang = session.get('detected_lang', 'en')
            session['lang'] = lang
            session.pop('manual_lang', None) # Re-enable auto mode
    
    # Fallback to session or default
    current_lang = session.get('lang', 'en')
    if current_lang not in TRANSLATIONS:
        current_lang = 'en'
    
    session['lang'] = current_lang
    # Build a mutable copy and backfill nav-header alias keys so every
    # language shows the correct Logout / Welcome text in layout.html.
    trans = dict(TRANSLATIONS[current_lang])
    if 'nav_logout' not in trans:
        trans['nav_logout'] = trans.get('logout', 'Logout')
    if 'nav_welcome' not in trans:
        trans['nav_welcome'] = trans.get('welcome', 'Welcome')
    if 'partner' not in trans:
        trans['partner'] = 'Partner'
    return trans, current_lang

def get_role():
    """Helper to get standardized role from session"""
    raw_role = session.get('role', 'farmer')
    return ROLE_MAP.get(raw_role, raw_role)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            _, lang = get_trans()
            flash("Please login to access this feature.", "error")
            return redirect(url_for('login', lang=lang))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            user_role = get_role()
            
            # Admin can access everything
            if user_role == 'admin' or user_role in roles:
                return f(*args, **kwargs)
            
            # Unified Portal Policy: allow any valid role into home/dashboard
            # This ensures roles don't get 'Access Denied' on their own start page
            if user_role in AQUA_ROLES and f.__name__ in ['home_page', 'api_home_data', 'farmer_hub', 'business_portal', 'expert_portal', 'api_aquacycle_dashboard']:
                return f(*args, **kwargs)
            
            flash(f"Access Denied: Your role ({user_role}) does not have permission for this portal.", "error")
            return redirect(url_for('portal_select'))
        return decorated_function
    return decorator
