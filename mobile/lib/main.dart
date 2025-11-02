import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/config/app_config.dart';
import 'package:buildsmart_mobile/core/http/api_client.dart';
import 'package:buildsmart_mobile/core/cache/cache_manager.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:buildsmart_mobile/core/routing/app_router.dart';

/// BuildSmart Mobile App Entry Point
/// 
/// Initializes app configuration, API client, and sets up Riverpod
/// for state management with go_router for navigation.
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables from .env file
  await AppConfig.instance.load();

  // Initialize cache
  await CacheManager.initialize();

  // Initialize API client
  ApiClient.instance.initialize();

  runApp(
    const ProviderScope(
      child: BuildSmartApp(),
    ),
  );
}

/// Main application widget
class BuildSmartApp extends ConsumerWidget {
  const BuildSmartApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);

    return MaterialApp.router(
      title: AppConfig.instance.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.light, // TODO: Add theme mode toggle
      routerConfig: router,
    );
  }
}
