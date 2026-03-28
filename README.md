<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a1628,40:003566,80:0077b6,100:00b4d8&height=230&section=header&text=🌊%20AQUA&fontSize=72&fontColor=ffffff&fontAlignY=38&desc=Smart%20Aquaculture%20Platform%20%E2%80%A2%20AI-Powered%20Predictions%20%E2%80%A2%20End-to-End%20Ecosystem&descAlignY=58&descSize=16&animation=fadeIn" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2500&pause=800&color=00B4D8&center=true&vCenter=true&width=750&lines=AI-Driven+Progressive+Web+App+for+Aquaculture+%F0%9F%A4%96;4+Proprietary+ML+Algorithms+%E2%80%94+88%E2%80%9395%25+Accuracy+%F0%9F%8E%AF;7+Role-Based+Stakeholder+Dashboards+%F0%9F%91%A5;Deployed+Live+on+Render+%F0%9F%9A%80" />

<br/><br/>

[![Live Demo](https://img.shields.io/badge/🔴%20Live%20Demo-aqua--ttiu.onrender.com-00b4d8?style=for-the-badge)](https://aqua-ttiu.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Bhogi123--T%2FAQUA-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Bhogi123-T/AQUA)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

![Python](https://img.shields.io/badge/Python-45.5%25-3776AB?style=flat-square&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-43.0%25-E34F26?style=flat-square&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-6.8%25-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-4.7%25-1572B6?style=flat-square&logo=css3&logoColor=white)

![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-Offline%20Ready-5A0FC8?style=flat-square&logo=pwa&logoColor=white)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=black)

</div>

---

## 📌 Overview

**AQUA** is a production-deployed, AI-driven Progressive Web App built to transform the aquaculture industry. It provides a complete end-to-end ecosystem — connecting farmers, hatcheries, buyers, lab technicians, and processing plants — with state-of-the-art ML-powered predictions for yield, disease, stocking density, and market pricing.

At its core are **4 proprietary machine learning algorithms** engineered specifically for aquaculture, delivering 85–95% accuracy across critical operational decisions.

> 🔴 **Live:** [aqua-ttiu.onrender.com](https://aqua-ttiu.onrender.com)

---

## 🧠 Proprietary ML Algorithms

AQUA ships with four custom hybrid algorithms designed from the ground up for aquaculture intelligence:

<br/>

| Algorithm | Full Name | Purpose | Accuracy |
|-----------|-----------|---------|----------|
| **ADER** | Aquaculture Decision Enhancement Regressor | Yield prediction & feed optimization using Random Forest + Gradient Boosting + Domain Feature Weighting | **92–95%** |
| **APDC** | Aqua Predictive Disease Classifier | Multi-class disease risk assessment with probability calibration | **88–91%** |
| **ASER** | Adaptive Stocking Ensemble Regressor | Optimal stocking density via environmental weighting & linear trend analysis | **90–93%** |
| **AMPRO** | Aqua Market Price Optimizer | Real-time buyer price prediction with market trend analysis & geographic normalization | **85–89%** |

---

## 👥 AQUA-Cycle — Role-Based Ecosystem

AQUA serves every stakeholder in the aquaculture supply chain with dedicated dashboards and workflows:

<br/>

```
👨‍🌾 Farmer          →  Pond management · Disease prediction · Feed tracking · Harvest listing
🏢 Hatchery         →  Seed batch creation · Delivery tracking
🧪 Lab Technician   →  Water & seed test results · Alert dispatch
🤝 Buyer/Exporter   →  Harvest browsing · International bulk orders
🏭 Processing Plant →  Seafood grading · Packaging · Shipping coordination
🚛 Contractor       →  Transport & harvest logistics management
⚡ Admin            →  Ecosystem oversight · Transaction monitoring
```

---

## ✨ Platform Capabilities

<table>
<tr>
<td width="50%" valign="top">

### 🤖 AI & Predictions
- Yield prediction with ADER (92–95% accuracy)
- Disease risk scoring with APDC (88–91%)
- Optimal stocking density via ASER (90–93%)
- Live market price forecasting via AMPRO (85–89%)

</td>
<td width="50%" valign="top">

### 🔗 Trade & Market
- Real-time market matrix
- Direct farmer-to-buyer trade engine
- International bulk order placement
- Live price tracking & geographic normalization

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🔒 Security & Auth
- OTP verification via Email & SMS (Twilio)
- Google OAuth 2.0 integration
- Protected role-based routes
- Supabase-backed session management

</td>
<td width="50%" valign="top">

### 🌐 Accessibility
- Progressive Web App — works offline
- Multi-language support (`core/translations.py`)
- Responsive across desktop & mobile
- PWA installable on any device

</td>
</tr>
</table>

---

## 🏗️ Project Structure

```
AQUA/
├── app.py                      # Main Flask application — routes & API endpoints
├── requirements.txt            # Python dependencies
├── vercel.json                 # Deployment configuration
├── .env.example                # Environment variables template
│
├── ml_core/
│   └── models/                 # Pre-trained .pkl ML models (ADER, APDC, ASER, AMPRO)
│
├── core/
│   └── translations.py         # Multi-language support configuration
│
├── data/
│   └── patches/                # Local JSON databases (users, community, trade data)
│
├── frontend/                   # Frontend assets & components
├── static/                     # CSS, JavaScript, PWA service worker & manifest
├── templates/                  # Jinja2 HTML templates
├── scripts/                    # Utility & automation scripts
└── docs/                       # Technical documentation
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Supabase account — [supabase.com](https://supabase.com) *(optional for cloud DB)*
- Twilio account *(for OTP via SMS)*
- Gmail app password *(for OTP via Email)*

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/Bhogi123-T/AQUA.git
cd AQUA

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# App
SECRET_KEY=your_secret_key

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Email OTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Twilio SMS OTP
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
```

### 3. Run Locally

```bash
python app.py
```

Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🌐 Deployment

AQUA is cloud-ready and has been deployed to Render:

| Platform | Purpose | Status |
|----------|---------|--------|
| **Render** | Full Flask backend + ML model serving | ✅ Live |
| **Supabase** | Database · Auth · Realtime | ✅ Active |
| **Vercel** | Static frontend (if decoupled) | ⚙️ Optional |

> **Live URL:** [aqua-ttiu.onrender.com](https://aqua-ttiu.onrender.com)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Flask |
| ML Models | scikit-learn · Random Forest · Gradient Boosting · Custom Ensembles |
| Database | Supabase (PostgreSQL) · Local JSON |
| Auth | Supabase Auth · Google OAuth 2.0 · Twilio OTP |
| Frontend | HTML5 · CSS3 · JavaScript |
| PWA | Service Worker · Web App Manifest |
| Deployment | Render · Vercel |

---

## 🤝 Contributing

Contributions are welcome — from bug fixes to new ML model integrations.

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: add your feature description"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00b4d8,50:0077b6,100:0a1628&height=130&section=footer&animation=fadeIn" />

**Built with ❤️ for the Aquaculture Industry**

*by [Bhogeswara Rao T](https://github.com/Bhogi123-T) · Chennai, India*

</div>
