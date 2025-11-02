import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';

/// Hero section widget with CTAs
/// 
/// Displays a large banner with construction imagery,
/// headline, and call-to-action buttons
class HeroSection extends StatelessWidget {
  const HeroSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 400,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            AppTheme.charcoalGray,
            AppTheme.charcoalGray.withValues(alpha: 0.8),
          ],
        ),
        image: DecorationImage(
          image: const NetworkImage(
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80',
          ),
          fit: BoxFit.cover,
          colorFilter: ColorFilter.mode(
            AppTheme.charcoalGray.withValues(alpha: 0.7),
            BlendMode.darken,
          ),
        ),
      ),
      child: Container(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 40),
            Text(
              'BuildSmart',
              style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    color: AppTheme.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 48,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              'Your One-Stop Construction Marketplace',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: AppTheme.white,
                    fontSize: 20,
                  ),
            ),
            const SizedBox(height: 24),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                ElevatedButton(
                  onPressed: () {
                    context.push(AppRoutes.search);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryYellow,
                    foregroundColor: AppTheme.charcoalGray,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                      vertical: 16,
                    ),
                    minimumSize: const Size(150, 48),
                  ),
                  child: const Text(
                    'Explore Materials',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                OutlinedButton(
                  onPressed: () {
                    context.push(AppRoutes.nearbyShops);
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppTheme.white,
                    side: const BorderSide(color: AppTheme.white, width: 2),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                      vertical: 16,
                    ),
                    minimumSize: const Size(150, 48),
                  ),
                  child: const Text(
                    'Find a Contractor',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

