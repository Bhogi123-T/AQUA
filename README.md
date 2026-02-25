# AQUA - Smart Aquaculture Platform

## 🌊 Overview

AQUA is an AI-powered Progressive Web App (PWA) for smart aquaculture management. It provides farmers, buyers, and technicians with real-time insights, predictive analytics, and mobile-first tools for optimizing aquaculture operations.

## ✨ Key Features

- **📱 QR Scanner**: Quick access to the platform via QR code scanning
- **🗑️ Data Management**: Clear cached data and reset the app
- **🧪 Disease Prediction**: AI-powered disease risk assessment
- **📍 Location Analysis**: Suitability analysis for aquaculture sites
- **🍽️ Feed Calculator**: Optimize feeding schedules and reduce costs
- **📈 Yield Forecasting**: Predict harvest yields
- **💰 Market Prices**: Real-time global market data
- **🌐 Offline Support**: Works without internet connection
- **🌍 Multi-language**: Supports 17+ languages

## 🚀 Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Mobile Access

- **Install as PWA**: Click the "Install App" button in the navigation
- **QR Scanner**: Navigate to the QR Scanner page to scan codes for quick access
- **Link**: https://aqua-ttiu.onrender.com/

## 📱 Mobile Features

### QR Scanner
Access the QR scanner from the navigation menu to:
- Scan QR codes to open URLs directly
- Quick access to https://aqua-ttiu.onrender.com/
- Camera-based scanning with auto-redirect

### Data Management
Clear all cached data including:
- LocalStorage
- IndexedDB
- Cache Storage
- Session data

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Models**: scikit-learn (joblib)
- **PWA**: Service Workers, Web App Manifest
- **QR Scanner**: html5-qrcode library

## 📂 Project Structure

```
AQUA-main/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── qr_scanner.html   # QR scanner page
│   ├── index.html        # Home page
│   └── ...
├── static/               # Static assets
│   ├── style.css        # Main stylesheet
│   ├── main.js          # JavaScript
│   ├── manifest.json    # PWA manifest
│   └── sw.js            # Service worker
├── Models/              # ML models
└── requirements.txt     # Python dependencies
```

## 🌐 Deployment

The app is configured for deployment on:
- **Render**: Free hosting (recommended)
- **Vercel**: Fast edge deployment
- **Local Network**: Access via IP address

## 📄 License

This project is open source and available for educational and commercial use.

## 🤝 Support

For issues or questions, please refer to the application's built-in help system or contact support.

---

**Made with ❤️ for the Aquaculture Industry**
