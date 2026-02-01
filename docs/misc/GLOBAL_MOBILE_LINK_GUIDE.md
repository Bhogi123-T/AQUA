# AquaSphere Global Mobile Link & QR Scanner

## Overview
A new mobile-first feature that provides:
- **Global Access Link**: Direct URL for accessing AquaSphere from any mobile device
- **QR Code Generator**: Auto-generated QR code for easy mobile scanning
- **Built-in QR Scanner**: Camera-based scanner to decode any AquaSphere QR codes
- **Copy to Clipboard**: Quick link sharing functionality

---

## Features

### 1. Global Access Link
- Unique, shareable URL that works on any device
- Language-aware (preserves user's selected language)
- Dynamically generated based on server URL
- Format: `http://localhost:5000/?lang=en`

### 2. QR Code Display
- Auto-generated QR code encoding the global link
- High error correction level (Level H) for reliability
- Clean white background for easy scanning
- Displays 250x250px on desktop, 200x200px on mobile

### 3. QR Scanner
- **Camera Access**: Uses device camera for live scanning
- **Environment Mode**: Prioritizes rear camera on mobile devices
- **Real-time Detection**: Uses jsQR library for fast decoding
- **Auto-Redirect**: Redirects to scanned URL automatically
- **Error Handling**: Graceful fallback if camera access denied
- **Stop Button**: Manual control to stop scanning session

### 4. Mobile Optimization
- Fully responsive design
- Touch-friendly buttons with large hit targets
- Portrait/landscape orientation support
- Offline-capable with Service Worker

---

## How to Use

### Accessing the Global Link Page
```
URL: http://localhost:5000/global-link
Or via navigation: Menu → Resources & Control → 📱 Global Link & Scanner
```

### Using the QR Generator
1. Navigate to the Global Link page
2. See the auto-generated QR code in the left panel
3. Copy the link using the "📋 Copy Link" button
4. Share via WhatsApp, Email, SMS, etc.

### Using the Scanner
1. Navigate to the Global Link page
2. Click "🎥 Start Camera" button
3. Grant camera permissions when prompted
4. Point camera at any AquaSphere QR code
5. Auto-redirect occurs when code is detected
6. Click "⛔ Stop Camera" to manually stop scanning

---

## API Endpoint

### Mobile Link Information API
```
GET /api/mobile-link?lang=en
```

**Response:**
```json
{
    "status": "success",
    "global_link": "http://localhost:5000/?lang=en",
    "scanner_link": "http://localhost:5000/global-link?lang=en",
    "platform": "AquaSphere",
    "version": "1.0",
    "timestamp": "2026-01-28T18:21:00.000000"
}
```

**Usage:**
- Third-party apps can fetch this to get current AquaSphere access URLs
- Useful for mobile app integration
- Returns JSON with both direct link and scanner link

---

## Technical Implementation

### Route Handler (app.py)
```python
@app.route("/global-link")
def global_link():
    """Mobile global access link with QR code and scanner"""
    trans, lang = get_trans()
    
    # Get the server URL dynamically
    server_url = request.host_url.rstrip('/')
    global_link_url = f"{server_url}/?lang={lang}"
    
    return render_template("global_link.html", 
                         trans=trans, 
                         lang=lang, 
                         global_link=global_link_url)
```

### Template (templates/global_link.html)
- Uses **QRCode.js** library for QR generation
- Uses **jsQR** library for QR scanning
- Uses **getUserMedia API** for camera access
- Canvas-based image processing for scan detection

### Key Libraries
1. **QRCode.js** (v1.0.0): QR code generation
2. **jsQR** (v1.4.0): QR code decoding
3. **Canvas API**: Real-time video processing
4. **getUserMedia API**: Camera access

---

## Mobile Optimization

### Responsive Breakpoints
- **Desktop**: Full two-column layout (QR + Scanner side-by-side)
- **Mobile (≤900px)**: Stacked single-column layout

### Touch Optimizations
- Large buttons: 1.5rem+ padding
- Increased font sizes: 1.5rem+ for readability
- Proper spacing between interactive elements
- Tap-friendly hit targets (>44px recommended)

### Offline Support
- Service Worker caches the global link page
- QR scanning works offline (after initial load)
- Camera access requires connection setup only

---

## User Flow Diagrams

### QR Code Generator Flow
```
User visits /global-link
    ↓
Receives dynamic server URL
    ↓
QR code auto-generated
    ↓
User can:
  → Copy link to clipboard
  → Share via social media
  → Scan with phone camera
  → Send via email/SMS
```

### QR Scanner Flow
```
Click "Start Camera"
    ↓
Browser requests camera permission
    ↓
Grant permission
    ↓
Live video feed displayed
    ↓
Point at QR code
    ↓
jsQR detects code
    ↓
Extract URL from data
    ↓
Show success message
    ↓
Auto-redirect after 2 seconds
```

---

## Security & Privacy

### Camera Permissions
- Only requested when user clicks "Start Camera"
- User can deny at browser prompt
- Permissions stored per-device/browser

### Data Privacy
- No QR code data sent to server
- All scanning happens client-side
- No tracking of scan history
- Language preference only

### HTTPS Deployment
- Ensure HTTPS in production for camera access
- Modern browsers require secure context for getUserMedia
- QR codes will work on both HTTP/HTTPS

---

## Troubleshooting

### Camera Not Working
**Problem**: "Unable to access camera" error
- **Solution 1**: Check browser camera permissions in settings
- **Solution 2**: Ensure HTTPS in production
- **Solution 3**: Try different browser
- **Solution 4**: Restart browser and refresh page

### QR Code Not Scanning
**Problem**: Scanner keeps running without detecting code
- **Solution 1**: Ensure QR code is well-lit
- **Solution 2**: Hold camera steady at 6-12 inches distance
- **Solution 3**: Try different angle
- **Solution 4**: Click "Stop Camera" and retry

### Link Not Copying
**Problem**: Copy button doesn't work
- **Solution 1**: Check browser clipboard permissions
- **Solution 2**: Try manual selection and Ctrl+C
- **Solution 3**: Refresh page and retry

---

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | getUserMedia fully supported |
| Firefox | ✅ Full | Camera access works well |
| Safari | ⚠️ Partial | Requires HTTPS, iOS 14.3+ |
| Edge | ✅ Full | Chromium-based, full support |
| Opera | ✅ Full | Chromium-based |
| IE 11 | ❌ None | No modern API support |

---

## Future Enhancements

- [ ] Generate custom QR codes with branding
- [ ] QR code download/print functionality
- [ ] Batch QR code generation for distribution
- [ ] Scan history/analytics
- [ ] Multi-format support (SMS, WiFi, vCard)
- [ ] Barcode scanning (1D codes)
- [ ] OCR text recognition from camera
- [ ] Screen sharing with QR overlay
- [ ] NFC tag integration
- [ ] Bluetooth device pairing

---

## File References

| File | Purpose |
|------|---------|
| [app.py](../app.py#L507) | Route handler for `/global-link` |
| [app.py](../app.py#L1355) | API endpoint `/api/mobile-link` |
| [templates/global_link.html](../templates/global_link.html) | Main template |
| [templates/layout.html](../templates/layout.html#L97) | Navigation link |
| [static/style.css](../static/style.css) | Already supports new layout |

---

## Testing Checklist

- [ ] Global link generates correctly
- [ ] QR code displays with correct URL
- [ ] Copy link button works on desktop
- [ ] Scanner starts with camera permission
- [ ] Scanner detects valid QR codes
- [ ] Auto-redirect works after scan
- [ ] Stop button halts camera stream
- [ ] Responsive on mobile devices (portrait/landscape)
- [ ] Works offline after initial load
- [ ] Language persistence maintained
- [ ] API endpoint returns correct JSON
- [ ] Error messages display properly

---

## Version Information
- **Feature Version**: 1.0
- **Created**: January 28, 2026
- **Compatible with**: AquaSphere v1.0+
- **Dependencies**: QRCode.js, jsQR, getUserMedia API

