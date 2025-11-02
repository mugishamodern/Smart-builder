# Recommended Packages

```
dependencies:
  flutter:
    sdk: flutter
  flutter_dotenv: ^5.1.0
  dio: ^5.4.0
  go_router: ^14.0.0
  flutter_riverpod: ^2.5.0 # or use bloc + flutter_bloc
  shared_preferences: ^2.2.3
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  google_maps_flutter: ^2.7.0
  geolocator: ^10.1.0
  url_launcher: ^6.3.0
  intl: ^0.19.0

dev_dependencies:
  flutter_lints: ^3.0.0
  build_runner: ^2.4.9
  freezed: ^2.5.2
  json_serializable: ^6.8.0
```

Notes:
- Choose one state management approach (Riverpod or Bloc) consistently.
- Consider `freezed` + `json_serializable` for models.
- If using Firebase for notifications, add `firebase_core` and `firebase_messaging`.
