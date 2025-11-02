import 'package:flutter/material.dart';

/// BuildSmart app theme configuration
/// 
/// Defines brand colors, typography, and UI component styling
/// matching the Flask web app design system.
class AppTheme {
  AppTheme._();

  // Brand Colors (matching Flask web app)
  static const Color primaryYellow = Color(0xFFFFB703); // #FFB703
  static const Color accentOrange = Color(0xFFFB8500); // #FB8500
  static const Color charcoalGray = Color(0xFF2F2F2F); // #2F2F2F
  static const Color bgLight = Color(0xFFF8F9FA); // #F8F9FA

  // Additional colors
  static const Color white = Color(0xFFFFFFFF);
  static const Color black = Color(0xFF000000);
  static const Color gray300 = Color(0xFFE0E0E0);
  static const Color gray500 = Color(0xFF9E9E9E);
  static const Color gray700 = Color(0xFF616161);

  /// Light theme
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.light(
        primary: primaryYellow,
        secondary: accentOrange,
        surface: white,
        error: Colors.red,
      ),
      scaffoldBackgroundColor: bgLight,
      appBarTheme: const AppBarTheme(
        backgroundColor: charcoalGray,
        foregroundColor: white,
        elevation: 0,
        centerTitle: true,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryYellow,
          foregroundColor: charcoalGray,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: charcoalGray,
        ),
        displayMedium: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: charcoalGray,
        ),
        displaySmall: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: charcoalGray,
        ),
        headlineMedium: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: charcoalGray,
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: charcoalGray,
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: charcoalGray,
        ),
      ),
      cardTheme: CardThemeData(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: gray300),
        ),
        filled: true,
        fillColor: white,
      ),
    );
  }

  /// Dark theme (optional - can be implemented later
  static ThemeData get darkTheme => lightTheme; // TODO: Implement dark theme if needed
}

