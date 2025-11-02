# Beta Distribution Guide

## Options

### Firebase App Distribution

1. **Setup Firebase Project**
   - Create project in Firebase Console
   - Add Android/iOS apps
   - Download config files

2. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

3. **Distribute Build**
   ```bash
   flutter build apk --release
   firebase appdistribution:distribute build/app/outputs/flutter-apk/app-release.apk \
     --app <APP_ID> \
     --groups "testers"
   ```

### TestFlight (iOS)

1. **Archive Build**
   ```bash
   flutter build ipa --release
   ```

2. **Upload to App Store Connect**
   - Use Transporter app or Xcode
   - Process in App Store Connect

3. **Create TestFlight Build**
   - Add internal/external testers
   - Configure testing details

### Google Play Internal Testing

1. **Create Internal Testing Track**
   - In Play Console
   - Upload APK/AAB
   - Add testers

2. **Share Testing Link**
   - Generate test link
   - Send to testers via email

## Beta Testing Checklist

- [ ] Build configured for testing
- [ ] Test devices registered
- [ ] Tester emails collected
- [ ] Test scenarios documented
- [ ] Feedback mechanism in place
- [ ] Crash reporting enabled
- [ ] Analytics configured
- [ ] Known issues documented

