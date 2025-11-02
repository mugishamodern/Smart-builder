import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';

/// Quick actions widget
/// 
/// Provides shortcuts to common actions
class QuickActions extends StatelessWidget {
  const QuickActions({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Quick Actions',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                _ActionButton(
                  icon: Icons.auto_awesome,
                  label: 'Get AI\nRecommendation',
                  color: Colors.blue,
                  onTap: () {
                    context.push('${AppRoutes.userRecommendations}/new');
                  },
                ),
                _ActionButton(
                  icon: Icons.search,
                  label: 'Browse\nProducts',
                  color: Colors.green,
                  onTap: () => context.push(AppRoutes.search),
                ),
                _ActionButton(
                  icon: Icons.build,
                  label: 'Find\nServices',
                  color: Colors.purple,
                  onTap: () {
                    context.push('/services');
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _ActionButton({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border.all(color: color.withValues(alpha: 0.3), width: 2),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(width: 12),
            Flexible(
              child: Text(
                label,
                style: const TextStyle(
                  fontWeight: FontWeight.w600,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                textAlign: TextAlign.left,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

