# How to Run BuildSmart Mobile App

## Running the App

When you run `flutter run`, you'll see a list of available devices:

```
[1]: Windows (windows)
[2]: Chrome (chrome)
[3]: Edge (edge)
```

### Recommended Options:

#### 1. **Windows Desktop** (Recommended for Development)
- Choose: `1` or `windows`
- Best for: Initial development and testing
- Closest to mobile experience on desktop
- Fast hot reload

#### 2. **Chrome Web** (Good for Quick Testing)
- Choose: `2` or `chrome`
- Best for: Quick web-based testing
- Note: Some mobile features may not work (maps, location)

#### 3. **Android Emulator** (Best for Mobile Testing)
If you have Android Studio installed:
- Open Android Studio
- Go to Tools > Device Manager
- Start an Android emulator
- Then run `flutter run` again

#### 4. **Physical Device**
- Connect your Android phone via USB
- Enable USB debugging
- Run `flutter run`

## Quick Commands

### Run on Specific Device:
```bash
# Windows
flutter run -d windows

# Chrome
flutter run -d chrome

# List available devices
flutter devices

# Run on first available device
flutter run
```

## After Running

Once the app starts:
- Press `r` to hot reload (apply changes quickly)
- Press `R` to hot restart (full restart)
- Press `q` to quit
- Press `h` for help

## Common Issues

### No Devices Found:
```bash
# Check connected devices
flutter devices

# If no Android emulator, start one:
# Android Studio > Tools > Device Manager > Start
```

### Build Errors:
```bash
# Clean build
flutter clean
flutter pub get
flutter run
```

### Hot Reload Not Working:
- Press `R` for full restart instead of `r`

## Next Steps

1. ✅ **Run the app**: Choose `1` for Windows or set up an emulator
2. 📱 **Test features**: Navigate through the app
3. 🔧 **Make changes**: Edit code and hot reload to see changes
4. 🚀 **Add features**: Start implementing from the TODO list

