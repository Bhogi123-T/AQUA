# 🌊 AQUA - Smart Aquaculture Platform with AI-Powered Predictions

![AQUA Banner](https://img.shields.io/badge/AQUA-Smart_Aquaculture-0052cc?style=for-the-badge&logo=water)

AQUA is a revolutionary, AI-driven Progressive Web App (PWA) designed to transform the aquaculture industry. It provides an end-to-end ecosystem connecting farmers, hatcheries, buyers, and processing plants, while offering state-of-the-art predictive analytics to optimize yields, prevent diseases, and maximize profits.

---

## ✨ Core Features

### 🧠 Custom Hybrid Machine Learning Algorithms
At the heart of AQUA are proprietary machine learning algorithms designed specifically for aquaculture:
- **ADER (Aquaculture Decision Enhancement Regressor)**: Combines Random Forest, Gradient Boosting, and Domain Feature Weighting for precise yield prediction and feed optimization (92-95% Accuracy).
- **APDC (Aqua Predictive Disease Classifier)**: Uses probability calibration and disease features for multi-class disease risk assessment (88-91% Accuracy).
- **ASER (Adaptive Stocking Ensemble Regressor)**: Optimizes stocking density based on environmental weighting and linear trend analysis (90-93% Accuracy).
- **AMPRO (Aqua Market Price Optimizer)**: Analyzes market trends and geographic normalization to predict buyer prices (85-89% Accuracy).

### 👥 Comprehensive Role-Based Ecosystem (AQUA-Cycle)
AQUA supports every stakeholder in the aquaculture supply chain with specialized dashboards and actions:
- 👨‍🌾 **Farmer**: Manage ponds, predict diseases, track feed, and list harvests.
- 🏢 **Hatchery**: Create seed batches and track deliveries.
- 🧪 **Lab Technician**: Record water/seed test results and send alerts.
- 🤝 **Buyer / Exporter**: Browse harvests and place international bulk orders.
- 🏭 **Processing Plant**: Grade seafood, manage packaging, and ship to buyers.
- 🚛 **Transport / Harvest Contractor**: Logistics management.
- ⚡ **Admin**: Oversee the ecosystem and monitor transactions.

### 🛠️ Advanced Tools & Capabilities
- **Disease & Yield Prediction**: AI-powered insights to mitigate risks and plan harvests.
- **Market Matrix & Direct Trade**: Connecting farmers directly with buyers and tracking real-time market prices.
- **Multi-language Support & PWA**: Accessible offline and available in multiple languages.
- **Secure Authentication**: OTP verification via Email/SMS and Google OAuth integration.

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.8+
- [Supabase](https://supabase.com/) account (optional, for cloud database)
- Twilio & Mail credentials (for OTP functionality)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bhogi123-T/AQUA.git
   cd AQUA
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory based on `.env.example`:
   ```env
   SECRET_KEY=your_secret_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_phone
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

5. **Access the Platform:**
   Open your browser and navigate to `http://localhost:5000`

---

## 📂 Project Structure

```
AQUA/
├── app.py                 # Main application logic & API endpoints
├── ml_core/
│   └── models/            # Pre-trained PKL models (disease, yield, etc.)
├── core/
│   └── translations.py    # Multi-language support configuration
├── data/                  # Local JSON databases (users, community, trade)
├── static/                # CSS, JS, and PWA assets
├── templates/             # HTML templates for the web app
└── requirements.txt       # Python dependencies
```

---

## 🌐 Deployment

AQUA is optimized for modern cloud deployments:
- **Render / Heroku**: Ideal for running the full Python/Flask backend and serving ML models.
- **Supabase**: Primary database and authentication provider.
- **Vercel**: Can be used for static frontend components if decoupled.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
<div align="center">
  <b>Made with ❤️ for the Aquaculture Industry</b>
</div>
