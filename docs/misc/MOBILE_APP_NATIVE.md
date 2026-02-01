# AquaSphere Mobile App Implementation Guide

## Overview
Convert AquaSphere web app to native mobile apps (iOS/Android) with full offline-first support using **Capacitor** - a framework that wraps web apps as native apps while maintaining offline functionality.

---

## Installation & Setup

### Prerequisites
```bash
npm --version          # v16+ required
node --version         # v18+ required
java -version         # For Android
```

### Step 1: Initialize Capacitor Project

```bash
cd c:\Users\bhoge\OneDrive\Documents\Desktop\AQUA

# Install Capacitor CLI globally
npm install -g @capacitor/cli

# Initialize Capacitor project
npx cap init AquaSphere com.aquasphere.mobile

# Add Android platform
npx cap add android

# Add iOS platform (macOS only)
# npx cap add ios
```

**What this creates:**
```
AQUA/
├── package.json (new)
├── ionic.config.json (optional)
├── android/ (native Android project)
├── ios/ (native iOS project - macOS only)
├── capacitor.config.ts (Capacitor configuration)
└── www/ (symlink to static files)
```

### Step 2: Create `package.json`

```json
{
  "name": "aquasphere",
  "version": "1.0.0",
  "description": "Offline-first aquaculture platform",
  "scripts": {
    "start": "python app.py",
    "build": "echo 'Flask app - no build needed'",
    "dev": "npm start",
    "android:build": "npx cap build android",
    "android:open": "npx cap open android",
    "android:sync": "npx cap sync android",
    "android:copy": "npx cap copy android",
    "ios:sync": "npx cap sync ios",
    "ios:open": "npx cap open ios"
  },
  "dependencies": {
    "@capacitor/app": "^5.0.0",
    "@capacitor/core": "^5.0.0",
    "@capacitor/camera": "^5.0.0",
    "@capacitor/filesystem": "^5.0.0",
    "@capacitor/network": "^5.0.0",
    "@capacitor/device": "^5.0.0",
    "@capacitor/geolocation": "^5.0.0"
  }
}
```

### Step 3: Create `capacitor.config.ts`

```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.aquasphere.mobile',
  appName: 'AquaSphere',
  webDir: 'static',  // Points to Flask static files
  server: {
    androidScheme: 'https',
    iosScheme: 'https',
    url: 'http://localhost:5000',  // Dev server
    cleartext: true  // Allow HTTP in dev
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#1a1a2e',
      showSpinner: true,
      spinnerColor: '#32CD32'
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#1a1a2e'
    }
  }
};

export default config;
```

---

## Android Native App Setup

### Method 1: Android Studio (Recommended)

```bash
cd c:\Users\bhoge\OneDrive\Documents\Desktop\AQUA

# Sync capacitor files to Android
npx cap sync android

# Open in Android Studio
npx cap open android
```

**Build Steps in Android Studio:**
1. File → Open → Select `android/` folder
2. Wait for Gradle sync
3. Select Device/Emulator
4. Click **Run** (Green Play Button)
5. App opens on device/emulator

### Method 2: Command Line

```bash
cd android

# Build APK for testing
./gradlew assembleDebug

# Build signed APK for release
./gradlew bundleRelease

# Output: android/app/build/outputs/apk/debug/app-debug.apk
```

### Android Permissions

Edit `android/app/src/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <!-- Internet & Offline -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <!-- Camera for photo predictions -->
    <uses-permission android:name="android.permission.CAMERA" />
    
    <!-- Location-based predictions -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    
    <!-- File storage for exports -->
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <!-- Background sync (future) -->
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    
    <application ... />
</manifest>
```

### Integrate Camera Plugin

```bash
npm install @capacitor/camera
npx cap sync android
```

Use in JavaScript:

```javascript
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

async function takePhoto() {
    const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: true,
        resultType: CameraResultType.Uri,
        source: CameraSource.Camera
    });
    
    console.log('Photo taken:', image);
    // Send to server or process locally
}
```

### Test on Android Device

```bash
# Enable USB debugging on Android device
adb devices  # List connected devices

# Install app
adb install android/app/build/outputs/apk/debug/app-debug.apk

# View logs
adb logcat | grep "AquaSphere"
```

---

## iOS Native App Setup (macOS Only)

```bash
# Sync to iOS
npx cap sync ios

# Open Xcode
npx cap open ios
```

**Build in Xcode:**
1. Select device or simulator
2. Product → Build
3. Product → Run
4. App opens on device

### iOS Permissions

Edit `ios/App/App/Info.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
    <dict>
        <!-- Camera -->
        <key>NSCameraUsageDescription</key>
        <string>AquaSphere uses camera for analyzing fish health</string>
        
        <!-- Location -->
        <key>NSLocationWhenInUseUsageDescription</key>
        <string>AquaSphere uses location for location-based predictions</string>
        
        <!-- Storage -->
        <key>NSLocalizedDescription</key>
        <string>AquaSphere stores data locally for offline access</string>
    </dict>
</plist>
```

---

## Enhanced Offline Features for Mobile

### 1. Device Sensors Integration

**Location-Based Predictions:**
```javascript
import { Geolocation } from '@capacitor/geolocation';

async function getLocationData() {
    const coordinates = await Geolocation.getCurrentPosition();
    const { latitude, longitude } = coordinates.coords;
    
    // Use location for regional prediction
    const prediction = await fetch('/predict_location', {
        method: 'POST',
        body: new FormData({
            latitude,
            longitude,
            species: 'Vannamei'
        })
    });
    
    return prediction.json();
}
```

**Camera Integration for Disease Detection:**
```javascript
import { Camera, CameraResultType } from '@capacitor/camera';

async function analyzeFishHealth() {
    const photo = await Camera.getPhoto({
        quality: 90,
        resultType: CameraResultType.Base64
    });
    
    // Send to server for ML analysis
    const result = await fetch('/analyze-fish-health', {
        method: 'POST',
        body: JSON.stringify({
            image: photo.base64String,
            species: selectedSpecies
        })
    });
    
    return result.json();
}
```

### 2. Network Status Monitoring

```javascript
import { Network } from '@capacitor/network';

async function monitorConnection() {
    Network.addListener('networkStatusChange', (status) => {
        console.log('Network status:', status);
        
        if (status.connected) {
            console.log('✅ Back online - syncing...');
            offlineManager.syncPendingData();
            
            // Show toast notification
            showNotification('Syncing offline predictions...', 'info');
        } else {
            console.log('📡 Offline mode activated');
            showNotification('Working offline - changes will sync later', 'info');
        }
    });
}

// Check current status
const status = await Network.getStatus();
console.log('Is connected:', status.connected);
```

### 3. Background Data Sync

```javascript
// iOS Background App Refresh (macOS only)
// Edit android/app/build.gradle:
dependencies {
    implementation 'com.google.android.gms:play-services-location:21.0.1'
}

// Enable background sync
async function enableBackgroundSync() {
    if (typeof ServiceWorkerRegistration !== 'undefined' && 
        'sync' in ServiceWorkerRegistration.prototype) {
        
        try {
            const registration = await navigator.serviceWorker.ready;
            await registration.sync.register('sync-predictions');
            console.log('Background sync registered');
        } catch (error) {
            console.log('Background sync not supported:', error);
        }
    }
}
```

### 4. Local File Storage for Exports

```javascript
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem';

async function exportPredictions() {
    const predictions = await offlineManager.getFromIndexedDB('predictions');
    
    const filename = `aquasphere-predictions-${new Date().toISOString()}.json`;
    
    const result = await Filesystem.writeFile({
        path: filename,
        data: JSON.stringify(predictions, null, 2),
        directory: Directory.Documents,
        encoding: Encoding.UTF8
    });
    
    console.log('Exported to:', result.uri);
    return result;
}
```

---

## Building Release Apps

### Android Release APK

```bash
cd android

# Create keystore (one-time)
keytool -genkey -v -keystore aquasphere-key.jks \
    -keyalg RSA -keysize 2048 -validity 10000

# Sign and build release APK
./gradlew bundleRelease -Pandroid.injected.signing.store.file=/path/to/aquasphere-key.jks \
    -Pandroid.injected.signing.store.password=PASSWORD \
    -Pandroid.injected.signing.key.alias=alias_name \
    -Pandroid.injected.signing.key.password=PASSWORD
```

**Output**: `android/app/build/outputs/bundle/release/app-release.aab`

Upload to **Google Play Store**.

### iOS Release

```bash
# Archive in Xcode
Product → Archive

# Export for distribution
Organizer → Right-click Archive → Distribute App

# Choose "App Store Connect"
# Follow prompts to upload
```

---

## Progressive Web App vs Native App

| Feature | PWA | Native |
|---------|-----|--------|
| Offline | ✅ | ✅ |
| Installation | ✅ Add to Home | ✅ App Store |
| Camera | ⚠️ Limited | ✅ Full |
| Location | ✅ | ✅ |
| Notifications | ⚠️ Push | ✅ Local/Push |
| File Access | Limited | ✅ Full |
| Performance | Good | Excellent |
| Development | 1x codebase | 2x codebases |

**Recommendation**: Start with PWA, transition to native when features require it.

---

## Testing Mobile App

### Android Emulator
```bash
# List available emulators
emulator -list-avds

# Run emulator
emulator -avd Pixel_6_API_33

# Install app
adb install app-debug.apk

# Test offline
adb shell cmd connectivity airplane-mode enable
# Use app...
adb shell cmd connectivity airplane-mode disable
```

### Real Device Testing
1. Enable USB Debugging on phone
2. Connect via USB
3. Run: `npx cap run android`
4. Toggle airplane mode to test offline
5. Check DevTools in Chrome: `chrome://inspect`

---

## Debugging Native App

### Android Logs
```bash
adb logcat | grep "AquaSphere"
```

### iOS Logs
```bash
# In Xcode
View → Debug Area → Show Console

# Or via terminal
log stream --predicate 'process == "AquaSphere"'
```

### DevTools in Native App
```bash
# Android: USB debug bridge
adb forward tcp:9222 localabstract:webview_devtools_remote_<app_id>

# Open in Chrome
chrome://inspect
```

---

## Troubleshooting

### App Won't Load
**Android:**
```bash
# Check if localhost server is accessible
adb shell ping host.docker.internal:5000

# Update capacitor.config.ts server.url if needed
```

**iOS:**
- Ensure WiFi and Mac are on same network
- Update Info.plist with server URL

### Offline Not Working
```javascript
// Check service worker in DevTools
navigator.serviceWorker.getRegistrations()

// Check IndexedDB
console.log(await offlineManager.getFromIndexedDB('disease'))
```

### Sync Failed
```javascript
// Manual sync trigger
offlineManager.syncPendingData().then(() => {
    console.log('Sync complete');
});
```

---

## Deployment Checklist

- [ ] App runs without internet
- [ ] All predictions work offline
- [ ] Data syncs when back online
- [ ] Notifications appear for sync status
- [ ] Camera works (Android/iOS)
- [ ] Location data collected properly
- [ ] App icon displays correctly
- [ ] Splash screen appears
- [ ] Release APK built and signed
- [ ] Tested on real device (not just emulator)
- [ ] Performance acceptable
- [ ] Storage under device limits

---

## Next Steps

1. ✅ **Setup Capacitor**: `npx cap init`
2. ✅ **Build Android**: `npx cap open android` + Build in Studio
3. ✅ **Test offline**: Toggle airplane mode
4. ✅ **Test sync**: Go online and check logs
5. 🚀 **Release**: Build signed APK and upload to Play Store
6. 📱 **Monitor**: Use Play Store console for crash reports

---

**Status**: Ready for Development | **Last Updated**: January 2026
