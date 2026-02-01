# Production URL Configuration - AquaSphere Mobile Global Link

## Current Configuration
**Production URL**: `https://aqua-ttiu.onrender.com`  
**Environment**: Render Cloud Deployment  
**Last Updated**: January 28, 2026

---

## Global Link Features

### 1. Main Global Link Page
**URL**: `https://aqua-ttiu.onrender.com/global-link`

Features:
- Full-featured QR code generator and scanner
- Side-by-side layout on desktop
- Stacked layout on mobile
- Copy-to-clipboard functionality
- Live camera scanner
- Environment badge showing production URL

**Best For**:
- Desktop users
- Desktop-to-mobile sharing
- Full feature access

### 2. Mobile Scanner (Lightweight)
**URL**: `https://aqua-ttiu.onrender.com/mobile-scanner`

Features:
- Optimized for mobile devices
- Minimal layout, fast loading
- Quick QR code display
- One-tap camera access
- Instant link sharing
- Reduced data usage

**Best For**:
- Mobile users
- Low bandwidth environments
- Quick access
- Direct mobile sharing

### 3. API Endpoint
**URL**: `https://aqua-ttiu.onrender.com/api/mobile-link?lang=en`

**Response**:
```json
{
    "status": "success",
    "global_link": "https://aqua-ttiu.onrender.com/?lang=en",
    "scanner_link": "https://aqua-ttiu.onrender.com/global-link?lang=en",
    "platform": "AquaSphere",
    "version": "1.0",
    "environment": "production",
    "timestamp": "2026-01-28T18:21:00.000000"
}
```

**Best For**:
- Third-party integrations
- Mobile apps
- API clients
- Programmatic access

---

## Production URL Deployment

### Files Modified
1. **config.json**
   - Added `PRODUCTION_URL` field
   - Value: `https://aqua-ttiu.onrender.com`

2. **app.py**
   - Updated `APP_CONFIG` to include `PRODUCTION_URL`
   - Modified `/global-link` route to use production URL
   - Modified `/mobile-scanner` route to use production URL
   - Modified `/api/mobile-link` endpoint to use production URL

3. **templates/global_link.html**
   - Added production environment badge
   - URL display shows full production URL
   - QR code encodes production URL

4. **templates/mobile_scanner.html**
   - Lightweight mobile version
   - Production URL embedded
   - Optimized for fast loading

---

## URL Routing

### User Flows

#### Desktop User
```
https://aqua-ttiu.onrender.com/
    ↓
Clicks "📱 Global Link & Scanner"
    ↓
https://aqua-ttiu.onrender.com/global-link
    ↓
Sees QR code and scanner
    ↓
Can copy link or scan QR codes
```

#### Mobile User
```
https://aqua-ttiu.onrender.com/
    ↓
Clicks "📱 Global Link & Scanner"
    ↓
https://aqua-ttiu.onrender.com/mobile-scanner
    ↓
Lightweight scanner interface
    ↓
Quick QR code access or camera scanner
```

#### Direct Mobile Scanner Access
```
https://aqua-ttiu.onrender.com/mobile-scanner
    ↓
Fast loading
    ↓
Display QR code + Copy/Scan buttons
    ↓
One-click camera access
```

---

## Configuration Details

### Environment Variables (Optional)
```bash
PRODUCTION_URL=https://aqua-ttiu.onrender.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
# ... other config vars
```

### Fallback URL
If `PRODUCTION_URL` is not set, defaults to:
```
https://aqua-ttiu.onrender.com
```

### Dynamic Detection
All routes use `APP_CONFIG.get("PRODUCTION_URL", ...)` for:
- Flexibility across environments
- Easy switching between dev/staging/prod
- No hardcoded localhost references

---

## Security Features

✅ **HTTPS Only**: Production URL is secure  
✅ **No localhost**: Removed all localhost references  
✅ **Client-side Scanning**: QR scanning happens on device  
✅ **Language Preservation**: User language maintained in URLs  
✅ **CORS Friendly**: API endpoint supports cross-origin requests  
✅ **Rate Limited**: Can add rate limiting via Render config  

---

## Mobile Optimization

### Responsive Design
- **Desktop**: Full featured at `/global-link`
- **Tablet**: Stacked layout with large buttons
- **Mobile**: Lightweight version at `/mobile-scanner`

### Performance
- Production URL cached by CDN
- Service Worker caches all pages
- QR generation is instant
- Camera access is lazy-loaded

### Accessibility
- Large buttons (1.5rem+ padding)
- High contrast colors
- Clear error messages
- Keyboard navigation support

---

## Testing Checklist

- [x] Production URL configured in config.json
- [x] app.py uses production URL correctly
- [x] `/global-link` displays production URL
- [x] `/mobile-scanner` displays production URL
- [x] `/api/mobile-link` returns production URL
- [x] QR codes encode production URLs
- [x] All localhost references removed
- [x] Navigation links updated
- [x] Environment badge displays correctly
- [x] Mobile scanner loads fast
- [x] Camera scanner works with production URL
- [x] Copy-to-clipboard works
- [x] Language parameter preserved
- [x] Responsive design verified

---

## How to Share

### Method 1: QR Code
1. Visit `https://aqua-ttiu.onrender.com/global-link`
2. Share QR code via screenshot/WhatsApp
3. Others scan to access instantly

### Method 2: Direct Link
1. Visit `https://aqua-ttiu.onrender.com/global-link`
2. Click "📋 Copy Link"
3. Share in chat, email, SMS
4. Recipient clicks to access

### Method 3: Mobile Scanner
1. Visit `https://aqua-ttiu.onrender.com/mobile-scanner`
2. Share this direct link with others
3. They get fast mobile interface

### Method 4: API Integration
1. Call `/api/mobile-link?lang=en`
2. Get JSON with all URLs
3. Integrate into your app
4. Direct users as needed

---

## Monitoring & Uptime

### Render Status
- Platform: Render.com
- Service: Web Service
- URL: https://aqua-ttiu.onrender.com
- Status Page: https://status.render.com

### Performance
- Global CDN: Included
- SSL/TLS: Auto-managed
- Deployment: Automatic on push

### Support
- Render Support: support@render.com
- Issue Tracker: GitHub Issues
- Monitoring: Uptime Robot

---

## Future Enhancements

- [ ] QR code download/print
- [ ] Custom branding options
- [ ] Batch QR generation
- [ ] Scan analytics
- [ ] Offline QR code storage
- [ ] Multiple environment support
- [ ] QR code expiration
- [ ] Usage statistics dashboard

---

## Related Documentation

- [GLOBAL_MOBILE_LINK_GUIDE.md](./GLOBAL_MOBILE_LINK_GUIDE.md) - Feature documentation
- [app.py](./app.py) - Route implementations
- [config.json](./config.json) - Configuration
- [templates/global_link.html](./templates/global_link.html) - Full QR/Scanner page
- [templates/mobile_scanner.html](./templates/mobile_scanner.html) - Mobile scanner

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial production URL setup |
| - | - | Removed localhost references |
| - | - | Added mobile-scanner route |
| - | - | Updated all routes to use production URL |
| - | - | Created configuration guide |

---

**Production Ready**: ✅ YES  
**Status**: 🟢 ACTIVE  
**Last Verified**: January 28, 2026

