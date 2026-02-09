# AquaSphere AI - Copilot Instructions

## Project Overview
**AquaSphere** is a multilingual AI-driven aquaculture ecosystem platform built with Flask. It combines ML-powered predictive models with real-time market data, expert connectivity, and IoT integration to assist global aquaculture farmers, buyers, and technicians.

**Tech Stack**: Python Flask, scikit-learn ML models, Jinja2 templates, JavaScript frontend, multi-language support (10+ languages), Twilio SMS/Email OTP, Vercel deployment.

---

## Architecture & Data Flows

### Core ML Prediction Pipeline
- **7 Independent ML Models** (under `ML/`): Each trained via `Datasets/generate_*.py` → `dataset/*.csv` → `models/*.pkl`
  - `disease_model.py`: Water parameters (temp, pH, DO, salinity, turbidity) → Disease Risk classification
  - `location_model.py`, `feed_model.py`, `yield_model.py`, `buyer_model.py`, `stocking_model.py`, `seed_model.py`
- **All models use RandomForestClassifier** with joblib serialization
- Routes load models at startup (lines 133-155 in app.py); predict routes are at `/predict_*` endpoints
- **No database**: All ML data persists in pickle files in `models/` directory

### Offline-First Architecture
- **Service Worker** (`static/sw.js`): Caches all assets and API responses for offline access
- **IndexedDB Storage** (`static/offline-manager.js`): Stores datasets locally on first visit
- **Offline Predictions**: When offline, predictions use dataset similarity matching instead of ML models
- **Auto-Sync**: Offline predictions saved to IndexedDB, synced to `/api/sync-prediction` when back online
- **Data Flow**: 
  1. First load (online) → Downloads datasets → Stores in IndexedDB via `OfflineManager`
  2. Form submit (offline) → `setupOfflineFormHandling()` intercepts → Calls `offlineManager.predict*()` → Displays demo result
  3. Back online → `syncPendingData()` syncs all cached predictions to server

### User Authentication & Session Management
- **Multi-step OTP flow** (email OR SMS via Twilio):
  1. User enters email/phone → `send_otp()` dispatches OTP
  2. `DEMO_MODE` bypasses real delivery (for testing)
  3. Session stores `pending_user`, `otp`, `user` (on success)
- **Persistence**: User profiles stored in `users.json` (JSON file-based, not DB)
- **Language preference**: Stored in session; defaults to English

### Multilingual Translation Architecture
- **Single source of truth**: `translations.py` contains full TRANSLATIONS dict (7,400+ lines)
- **Key naming convention**: `{category}_{item_name}` (e.g., `species_rohu`, `region_andhra_pradesh`)
- **Template injection**: `@app.context_processor` creates `translate_species()`, `translate_region()`, `translate_tip()` helpers
- **Lazy translation**: Keys not found return original text (graceful fallback)
- **Patch system**: `patches/` contains JSON files for bulk language additions (e.g., `patch_new_langs_full.json`)
- **Scripts**: `scripts/apply_patches.py`, `scripts/generate_missing_keys.py` for maintenance

### Global Reference Data (In-Memory)
- **GLOBAL_AQUA_REGIONS**: Hardcoded geographic hierarchy (Country → State → District) for 9 regions
- **SPECIES_META**: Emoji mappings for 24 aquaculture species
- **PRECAUTIONS**: Domain-specific knowledge (Water Management, Disease Mitigation, Management) with translated tips
- **SEASONAL_ADVICE**: Per-season species recommendations (temperature-based)
- **SPECIES_RULES**: Min/max thresholds for salinity/pH/temperature by species

### Request Flow & Result Rendering
- Prediction endpoints (`/predict_*`) receive form data → run model inference → render `result.html` with formatted output
- **Exception handling**: Try-catch blocks default to demo values if model inference fails (production resilience)
- All predictions include currency conversion (USD to INR: 1:83 rate, hardcoded line 189)

---

## Critical Developer Workflows

### Adding a New Prediction Feature
1. **Create dataset generator**: `Datasets/generate_newfeature.py` → outputs `dataset/newfeature.csv`
2. **Train model**: `ML/newfeature_model.py` → loads CSV, trains RandomForest, saves to `models/newfeature.pkl`
3. **Load model in app.py** (line ~133): `newfeature_model = joblib.load("models/newfeature.pkl")`
4. **Add route** (e.g., `/predict_newfeature`):
   - Extract form data from `request.form.get()`
   - Preprocess inputs via label encoders (e.g., `le_country.transform()`)
   - Call `newfeature_model.predict()`
   - Render result with translation key lookups
5. **Add template**: Create `templates/newfeature.html` with form inputs matching model feature expectations
6. **Add translations**: Update `translations.py` with keys like `newfeature_title`, `newfeature_desc`, field labels

### Running Locally
```bash
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000
```
- Models must exist in `models/` directory before startup (pregenerated via ML scripts)
- No build step needed; Jinja2 templates auto-compile
- Service Worker automatically caches assets on first visit

### Testing Offline Mode Locally
1. Start the app normally: `python app.py`
2. Visit http://localhost:5000 to load datasets into IndexedDB
3. Open DevTools (F12) → Application → Service Workers → Check "Offline" checkbox
4. Try submitting a prediction form → Uses cached data instead of making requests
5. Check Console for `OfflineManager initialized` message

### Deployment to Vercel
- Configured in `vercel.json`: Python runtime, static file routing
- Environment variables: Set via Vercel dashboard (`MAIL_SERVER`, `TWILIO_ACCOUNT_SID`, etc.)
- Read-only filesystem: `save_json()` calls wrapped in try-catch (lines 37-41); Vercel fails silently on file persistence
- **Important**: All writable state (users.json, config.json) should use cloud storage in production
- **Offline Support**: Service Worker caches will persist across deployments

---

## Project-Specific Conventions

### Translation Key Patterns
- **Navigation**: `nav_{section}` (e.g., `nav_farmer`, `nav_market`)
- **Species**: `species_{species_name_lowercase_underscored}` (e.g., `species_vannamei`, `species_mud_crab`)
- **Regions**: `region_{region_name_lowercase_underscored}` (e.g., `region_andhra_pradesh`)
- **Categories**: `cat_{category_lowercase}` (e.g., `cat_water_management`)
- **Tips/Advice**: `tip_{slugified_text}` (spaces/punctuation → underscores)
- **Error messages**: `err_{error_type}` (e.g., `err_email_fail`, `err_not_found`)

### HTML Template Structure
- **Layout base**: `templates/layout.html` (header, nav, footer; includes language switcher)
- **All pages extend layout**: `{% extends "layout.html" %}`
- **Form submissions**: Use `POST` to `/predict_*` endpoints
- **Result display**: Redirects to `result.html` with `title`, `description`, `result` variables
- **Static assets**: CSS in `static/style.css`, JS in `static/main.js`; images in `static/img/`

### Error Handling Conventions
- **Silent failures**: Model loading errors, Twilio/Mail failures wrapped in try-catch; app starts anyway
- **Demo mode fallback**: Set `DEMO_MODE: true` in config to bypass real OTP/SMS/Email
- **Graceful degradation**: Missing translations → return original text; missing models → demo results

### Data Validation
- **File uploads**: Only `ALLOWED_EXTENSIONS` (images/video, line 26) permitted
- **OTP format**: 6-digit random (lines 363, 401)
- **Form inputs**: Minimal validation; ML models handle numeric type coercion
- **No SQL injection risk**: No SQL database used; JSON files are safe

### Performance Considerations
- **Model loading**: All 7 models + 21 label encoders loaded at app startup (one-time cost)
- **Caching**: None; every request re-reads global data structures (not a bottleneck for current scale)
- **API calls**: Weather endpoint (wttr.in) has 2-second timeout; fails gracefully (line 480)

---

## Integration Points & External Dependencies

### Third-Party Services
- **Twilio**: SMS delivery (Client initialization line 73); credentials from env vars
- **Flask-Mail**: Email OTP delivery; SMTP config from env vars; requires active mail credentials
- **Weather API**: `wttr.in` (free, no auth) for live weather; used on homepage (line 480)

### Offline Storage APIs (Browser)
- **IndexedDB**: Persistent local storage for datasets (OfflineManager class in `static/offline-manager.js`)
- **Service Worker Cache API**: Caches HTTP responses, static assets for offline access
- **localStorage**: Session metadata, last sync timestamps

### Environment Variables Required
```
MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
```

### API Endpoints for Offline Support
- `GET /api/dataset/{name}` - Returns CSV data as JSON (disease, location, feed, yield, buyer, stocking, seed)
- `POST /api/sync-prediction` - Receives offline predictions from client for server-side logging
- `GET /offline-status` - Dashboard showing cached datasets and synced predictions

### Cross-Component Communication
- **Session → Translation**: `request.args.get('lang')` or `session.get('lang')`
- **Form → Model**: HTML forms post to `/predict_*` → raw form data passed to sklearn predict
- **Result → Template**: Prediction results injected into `result.html` context dict

---

## When Modifying Code

### Adding a New Language
1. Add language code (e.g., `'zh'`) to `TRANSLATIONS` dict in `translations.py`
2. Add all key-value translations OR use patch system:
   - Create `patches/patch_LANG.json` with `{"key": "translation"}` pairs
   - Run `python scripts/apply_patches.py`
3. Update language dropdown in `templates/layout.html` (if not auto-generated)

### Adding a New Region/District
1. Add to `GLOBAL_AQUA_REGIONS` dict (line 197 in app.py)
2. Add translation keys: `region_country`, `region_state`, `region_district` in `translations.py`

### Debugging Model Predictions
- Add `print()` statements in `/predict_*` routes before `model.predict()`
- Check input shape matches training data (e.g., disease model expects 5 features: temp, pH, DO, salinity, turbidity)
- Verify label encoders are initialized and used correctly (e.g., `le_country.transform(['India'])`)

### Testing Locally Without Real Services
- Set `"DEMO_MODE": true` in config.json or via settings UI
- OTPs bypass real email/SMS; use any string as "OTP"
- Market data uses hardcoded base values with random ±2% fluctuation

---

## Key Files Reference

| File | Purpose |
|------|---------|
| [app.py](app.py) | Main Flask app (1250+ lines); all routes, model loading, auth, offline API endpoints |
| [static/offline-manager.js](static/offline-manager.js) | IndexedDB manager; handles offline predictions, dataset caching, sync logic |
| [static/sw.js](static/sw.js) | Service Worker; caches assets, API responses, enables offline functionality |
| [static/main.js](static/main.js) | Frontend logic; form interception, offline fallbacks, PWA install |
| [static/manifest.json](static/manifest.json) | PWA manifest; app metadata, shortcuts, offline support declaration |
| [translations.py](translations.py) | 10+ language translations (7402 lines) |
| [templates/offline_status.html](templates/offline_status.html) | Dashboard showing cached data, sync status, offline capabilities |
| [config.py](config.py) | Dataset/model paths |
| [ML/](ML/) | 7 model training scripts (RandomForest) |
| [Datasets/](Datasets/) | Dataset generators; create CSVs from synthetic data |
| [templates/](templates/) | Jinja2 templates; 30+ pages + guides subdirectory |
| [static/style.css](static/style.css) | Global styling |
| [patches/](patches/) | Bulk translation JSON patches |
| [scripts/](scripts/) | Translation & data maintenance utilities |

---

## Known Limitations & TODOs

- **No real database**: Scalability limited; consider PostgreSQL for production
- **Model persistence**: No versioning; cannot roll back model retraining
- **File uploads**: Uploaded files not integrated with ML (stored but not used)
- **Session storage**: In-memory Flask sessions; lost on server restart
- **Security**: Settings page allows config changes without authentication (mentioned line 437)

---

## Testing New Features

When adding ML predictions or features:
1. Generate synthetic dataset: `python Datasets/generate_newfeature.py`
2. Train model: `python ML/newfeature_model.py`
3. Add route & template
4. Test locally: Verify form submission → model inference → result display
5. Check translations: All keys present in `translations.py`
6. Verify Vercel deploy: Static assets load; no file I/O errors

---

**Last Updated**: Jan 2026 | **Primary Language**: Python 3.8+ | **Deployment**: Vercel (serverless)
