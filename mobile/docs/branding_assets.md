# Branding Assets Guide

## Required Assets

### App Icons

#### Android
- **Adaptive Icon (Foreground)**: 1024x1024px PNG
  - Location: `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png`
- **Adaptive Icon (Background)**: 1024x1024px PNG
  - Location: `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_background.png`
- **Legacy Icon**: 512x512px PNG
  - Location: `android/app/src/main/res/mipmap-mdpi/ic_launcher.png`

#### iOS
- **App Icon**: 1024x1024px PNG (no transparency)
  - Location: `ios/Runner/Assets.xcassets/AppIcon.appiconset/`

### Splash Screens

#### Android
- **Launch Screen**: Create in `android/app/src/main/res/drawable/launch_background.xml`
- **Branded Splash**: Optional branded image

#### iOS
- **Launch Screen**: Configure in `ios/Runner/Base.lproj/LaunchScreen.storyboard`
- **Launch Image**: 2048x2732px for iPad Pro 12.9"

### Store Assets

#### Google Play Store
- **Feature Graphic**: 1024x500px PNG
- **Phone Screenshots**: 
  - Minimum: 2 screenshots
  - Recommended sizes: 1080x1920px or 1440x2560px
- **Tablet Screenshots** (if applicable):
  - Recommended: 1920x1200px or 2560x1600px

#### App Store
- **App Preview Videos** (optional): 15-30 seconds
- **Screenshots** (all required device sizes):
  - iPhone 6.7": 1290x2796px
  - iPhone 6.5": 1242x2688px
  - iPhone 5.5": 1242x2208px
  - iPad Pro 12.9": 2048x2732px

## Brand Colors

Based on construction theme:
- **Primary Yellow**: `#FFB703`
- **Accent Orange**: `#FB8500`
- **Charcoal Gray**: `#2F2F2F`
- **Background Light**: `#F8F9FA`

## Typography

- **Primary Font**: Poppins
- **Secondary Fonts**: Inter, Roboto

## Guidelines

1. Icons should be simple and recognizable at small sizes
2. Use brand colors consistently
3. Maintain high contrast for accessibility
4. Test icons on actual devices before submission
5. Ensure splash screens load quickly (< 2 seconds)

