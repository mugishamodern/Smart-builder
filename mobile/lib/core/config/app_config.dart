import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Application configuration singleton
/// 
/// Loads environment variables from .env file and provides
/// centralized access to configuration values throughout the app.
class AppConfig {
  AppConfig._();

  static AppConfig? _instance;
  static AppConfig get instance {
    _instance ??= AppConfig._();
    return _instance!;
  }

  /// Initialize configuration from .env file
  /// 
  /// Should be called in main() before runApp()
  /// The .env file should be in the project root and added to pubspec.yaml assets
  Future<void> load() async {
    try {
      await dotenv.load(fileName: '.env');
    } catch (e) {
      // If .env file is missing, use default values
      // This allows the app to run without .env in development
      print('Warning: .env file not found. Using default values.');
    }
  }

  // API Configuration
  String get apiBaseUrl => dotenv.env['API_BASE_URL'] ?? 'http://localhost:5000';
  
  // Google Maps
  String get googleMapsApiKey => dotenv.env['GOOGLE_MAPS_API_KEY'] ?? '';
  
  // App Info
  String get appName => dotenv.env['APP_NAME'] ?? 'BuildSmart';
  String get appVersion => dotenv.env['APP_VERSION'] ?? '1.0.0';
  
  // Feature Flags
  bool get enableOfflineCache => dotenv.env['ENABLE_OFFLINE_CACHE'] == 'true';
  bool get enablePushNotifications => dotenv.env['ENABLE_PUSH_NOTIFICATIONS'] == 'true';
  
  /// Check if configuration is valid
  bool get isValid {
    return apiBaseUrl.isNotEmpty && googleMapsApiKey.isNotEmpty;
  }
}

