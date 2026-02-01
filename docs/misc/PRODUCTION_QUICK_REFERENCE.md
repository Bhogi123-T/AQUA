# 🚀 Production URL Quick Reference

## Your Production URL
```
https://aqua-ttiu.onrender.com
```

---

## Three Ways to Access the Scanner

### 1️⃣ Full-Featured Desktop Scanner
```
https://aqua-ttiu.onrender.com/global-link
```
- Desktop layout (side-by-side QR + Scanner)
- Mobile layout (stacked)
- Copy link button
- Environment badge
- Full control

### 2️⃣ Fast Mobile Scanner
```
https://aqua-ttiu.onrender.com/mobile-scanner
```
- Optimized for mobile
- Minimal, fast loading
- One-click camera access
- Best for sharing on phones

### 3️⃣ JSON API Endpoint
```
https://aqua-ttiu.onrender.com/api/mobile-link?lang=en
```
- Returns JSON with all URLs
- For programmatic access
- Language parameter support
- Third-party app integration

---

## Share Your App

### Via QR Code
1. Go to: https://aqua-ttiu.onrender.com/global-link
2. Take screenshot of QR code
3. Share on WhatsApp/Instagram
4. Others scan → direct access

### Via Link
1. Go to: https://aqua-ttiu.onrender.com/global-link
2. Click "📋 Copy Link"
3. Paste in chat/email/SMS
4. Others click → direct access

### Via Mobile Scanner
1. Share: https://aqua-ttiu.onrender.com/mobile-scanner
2. Others open link
3. Click "🎥 Scan QR Code"
4. Point at any QR code → auto-redirect

---

## Features

✅ QR Code Generator  
✅ Mobile-Optimized  
✅ Camera Scanner  
✅ Copy to Clipboard  
✅ Offline Support  
✅ Multi-Language  
✅ HTTPS Secure  
✅ No Localhost  

---

## File Locations

| File | Purpose |
|------|---------|
| config.json | Production URL config |
| app.py | Routes & API |
| global_link.html | Full page |
| mobile_scanner.html | Mobile version |

---

## Environment Variable (Optional)

```bash
export PRODUCTION_URL=https://aqua-ttiu.onrender.com
```

---

## API Response Example

```json
{
    "status": "success",
    "global_link": "https://aqua-ttiu.onrender.com/?lang=en",
    "scanner_link": "https://aqua-ttiu.onrender.com/global-link?lang=en",
    "platform": "AquaSphere",
    "version": "1.0",
    "environment": "production",
    "timestamp": "2026-01-28T18:25:00.000000"
}
```

---

## Browser Support

| Chrome | Firefox | Safari | Edge | Opera |
|--------|---------|--------|------|-------|
| ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Troubleshooting

### Camera Not Working
→ Use HTTPS (production does, localhost won't work)

### QR Won't Scan
→ Better lighting, hold closer, clearer QR

### Link Won't Copy
→ Grant clipboard permissions, refresh

---

## Sharing Templates

### WhatsApp Message
```
Check out AquaSphere! 
Scan this QR: [screenshot]
Or visit: https://aqua-ttiu.onrender.com
```

### Email Template
```
Subject: AquaSphere - Global Aquaculture Platform

Hi!

Check out AquaSphere for smart aquaculture:
https://aqua-ttiu.onrender.com

You can also scan the QR code or use the mobile scanner:
https://aqua-ttiu.onrender.com/mobile-scanner

Features:
- AI-powered predictions
- Real-time market data
- Expert connectivity
- Multi-language support

Try it now!
```

### LinkedIn Post
```
🌍 Just launched AquaSphere's global mobile access link!

📱 Quick scan, instant access:
https://aqua-ttiu.onrender.com

🔍 Try the mobile scanner:
https://aqua-ttiu.onrender.com/mobile-scanner

Bringing smart aquaculture to farmers worldwide 🐠✨

#Aquaculture #AI #FoodTech
```

---

## Key Info

| Property | Value |
|----------|-------|
| **URL** | https://aqua-ttiu.onrender.com |
| **Platform** | Render.com |
| **Environment** | Production |
| **Status** | 🟢 Active |
| **HTTPS** | ✅ Enabled |
| **Language** | 10+ Supported |
| **Offline** | ✅ Supported |

---

## Desktop Menu Path

```
🏠 Home
→ ≡ Menu (Hamburger)
→ Resources & Control
→ 📱 Global Link & Scanner
```

---

## Localhost vs Production

### Localhost Development
- URL: `http://localhost:5000`
- QR codes encode: `https://aqua-ttiu.onrender.com`
- Cannot use camera (HTTP restriction)
- Great for development

### Production
- URL: `https://aqua-ttiu.onrender.com`
- QR codes encode: `https://aqua-ttiu.onrender.com`
- Camera works (HTTPS)
- Full functionality

---

## Success Indicators ✅

- [ ] Can access: https://aqua-ttiu.onrender.com/global-link
- [ ] See QR code on page
- [ ] See production URL
- [ ] Copy link button works
- [ ] Camera scanner starts on mobile
- [ ] QR codes redirect to production URL
- [ ] Mobile scanner loads fast
- [ ] API returns correct JSON

---

**Everything is configured. You're ready to go! 🚀**

Questions? Check the documentation files:
- PRODUCTION_URL_CONFIG.md
- PRODUCTION_URL_IMPLEMENTATION.md
- GLOBAL_MOBILE_LINK_GUIDE.md

