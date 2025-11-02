# Localization Setup

## Current Status

- **Default Language**: English (en)
- **Supported Locales**: English only (ready for expansion)

## Setup for Additional Languages

### 1. Add flutter_localizations

Update `pubspec.yaml`:
```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0
```

### 2. Configure App Localization

Update `main.dart`:
```dart
import 'package:flutter_localizations/flutter_localizations.dart';

MaterialApp(
  localizationsDelegates: [
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: [
    Locale('en', 'US'), // English
    Locale('sw', 'KE'), // Swahili (Kenya)
    // Add more locales as needed
  ],
)
```

### 3. Create Translation Files

Structure:
```
lib/l10n/
  app_en.arb
  app_sw.arb
```

### 4. Extract Strings

Use `flutter gen-l10n` or `intl_translation` package to extract translatable strings.

## Future Localization

To add a new language:
1. Create translation ARB file
2. Add locale to `supportedLocales`
3. Update all user-facing strings to use localization keys
4. Test with device language changes

