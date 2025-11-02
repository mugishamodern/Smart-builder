# Environment Configuration Guide

## Current Setup

Your `.env` file is configured with **default development values** that will work for local development.

### Default Values (Ready to Use)

- **API_BASE_URL**: `http://localhost:5000` 
  - This points to your Flask backend running locally
  - ✅ **This works right now** if your Flask backend is running on localhost:5000

- **GOOGLE_MAPS_API_KEY**: `your_google_maps_api_key_here`
  - This is a placeholder
  - ⚠️ **Maps features won't work** until you add a real API key
  - The rest of the app will work fine without it

## Getting Your Actual Values

### 1. API Base URL

#### For Local Development:
- **Windows/Mac/Linux**: Use `http://localhost:5000` (already set)
- **Android Emulator**: Use `http://10.0.2.2:5000` 
  - (Android emulator uses `10.0.2.2` instead of `localhost`)
- **iOS Simulator**: Use `http://localhost:5000` (same as your machine)

#### To Test Your Flask Backend:
```bash
# In your Flask project directory (buildsmart/)
cd buildsmart
python run.py
# Flask should start on http://localhost:5000
```

#### For Production (Later):
When you deploy your Flask backend, update to:
```
API_BASE_URL=https://your-production-domain.com
```

### 2. Google Maps API Key (Optional but Recommended)

You'll need this for:
- Maps showing nearby shops
- Location-based features
- Geolocation features

#### Steps to Get Google Maps API Key:

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com/google/maps-apis/credentials

2. **Create a Project** (if you don't have one):
   - Click "Create Project"
   - Name it (e.g., "BuildSmart")
   - Click "Create"

3. **Enable Required APIs**:
   - Go to "APIs & Services" > "Library"
   - Enable these APIs:
     - ✅ **Maps SDK for Android** (for Android app)
     - ✅ **Maps SDK for iOS** (for iOS app)
     - ✅ **Geocoding API** (for address lookup)
     - ✅ **Places API** (for nearby places)

4. **Create API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated key

5. **Restrict the Key** (Recommended for Production):
   - Click on the created key
   - Under "API restrictions":
     - Select "Restrict key"
     - Check only the APIs you enabled above
   - Under "Application restrictions":
     - For Android: Add your package name: `com.buildsmart.buildsmart_mobile`
     - For iOS: Add your bundle ID

6. **Add to .env**:
   ```
   GOOGLE_MAPS_API_KEY=paste_your_key_here
   ```

## Quick Start (Development)

You can start using the app **right now** with these defaults:

1. ✅ **Start your Flask backend**:
   ```bash
   cd buildsmart
   python run.py
   ```

2. ✅ **Run the Flutter app**:
   ```bash
   cd mobile
   flutter run
   ```

The app will connect to `http://localhost:5000` automatically.

⚠️ **Note**: Maps features will not work until you add a Google Maps API key, but everything else will work fine.

## For Android Emulator

If you're testing on an Android emulator, update `.env`:

```env
API_BASE_URL=http://10.0.2.2:5000
```

Then restart the app.

## Troubleshooting

### Can't Connect to Backend?

1. **Check Flask is running**:
   ```bash
   # Should show: Running on http://127.0.0.1:5000
   ```

2. **Check the URL in `.env`**:
   - Use `localhost` for Windows/Mac/Linux
   - Use `10.0.2.2` for Android emulator

3. **Check Firewall**:
   - Make sure port 5000 is not blocked

4. **Test with Browser**:
   - Visit `http://localhost:5000` in your browser
   - Should see your Flask app

### Maps Not Working?

- This is expected if you haven't added a Google Maps API key
- All other features will work fine
- Add the API key when you're ready to test maps

## Next Steps

1. ✅ **Start developing** - The app works with current defaults
2. 📍 **Add Google Maps key** - When you need maps/location features
3. 🚀 **Update for production** - When deploying to production

Your app is ready to use with the current `.env` configuration!

