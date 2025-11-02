import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/auth/providers/auth_provider.dart';
import 'package:buildsmart_mobile/features/user_dashboard/data/repositories/user_dashboard_repository.dart';
import 'package:buildsmart_mobile/features/user_dashboard/providers/user_dashboard_provider.dart';
import 'package:buildsmart_mobile/features/user_dashboard/presentation/widgets/stats_card.dart';
import 'package:buildsmart_mobile/features/user_dashboard/presentation/widgets/recent_orders_list.dart';
import 'package:buildsmart_mobile/features/user_dashboard/presentation/widgets/recent_recommendations_list.dart';
import 'package:buildsmart_mobile/features/user_dashboard/presentation/widgets/quick_actions.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:go_router/go_router.dart';

/// User dashboard page
/// 
/// Displays user stats, recent orders, saved recommendations, and quick actions
class UserDashboardPage extends ConsumerWidget {
  const UserDashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentUser = ref.watch(currentUserProvider);
    final dashboardData = ref.watch(dashboardDataProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () => context.push(AppRoutes.search),
            tooltip: 'Search',
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(dashboardDataProvider);
          await ref.read(dashboardDataProvider.future);
        },
        child: dashboardData.when(
          data: (data) => _buildDashboardContent(context, ref, currentUser, data),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) {
            final isAuthError = err.toString().contains('Authentication') || 
                               err.toString().contains('401') ||
                               err.toString().contains('Please log in');
            
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error_outline, size: 48, color: Colors.red),
                    const SizedBox(height: 16),
                    Text(
                      'Error: ${err.toString()}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 16),
                    ),
                    const SizedBox(height: 24),
                    if (isAuthError) ...[
                      ElevatedButton.icon(
                        onPressed: () => context.push(AppRoutes.login),
                        icon: const Icon(Icons.login),
                        label: const Text('Go to Login'),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        ),
                      ),
                      const SizedBox(height: 12),
                    ],
                    ElevatedButton(
                      onPressed: () => ref.refresh(dashboardDataProvider),
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildDashboardContent(
    BuildContext context,
    WidgetRef ref,
    AsyncValue<UserModel?> currentUser,
    DashboardData data,
  ) {
    final userName = currentUser.valueOrNull?.fullName ??
        currentUser.valueOrNull?.username ??
        'User';

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome header
          Text(
            'Welcome, $userName!',
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 8),
          Text(
            'Manage your construction projects and orders',
            style: TextStyle(color: Colors.grey[600]),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 24),

          // Statistics cards
          _buildStatsCards(context, data.stats),

          const SizedBox(height: 24),

          // Quick actions
          const QuickActions(),

          const SizedBox(height: 24),

          // Recent recommendations and orders
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: RecentRecommendationsList(
                  recommendations: data.savedRecommendations,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: RecentOrdersList(
                  orders: data.recentOrders,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatsCards(BuildContext context, DashboardStats stats) {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      childAspectRatio: 1.5,
      children: [
        StatsCard(
          title: 'Recommendations',
          value: stats.totalRecommendations.toString(),
          icon: Icons.auto_awesome,
          color: Colors.blue,
        ),
        StatsCard(
          title: 'Orders',
          value: stats.totalOrders.toString(),
          icon: Icons.shopping_cart,
          color: Colors.green,
        ),
        StatsCard(
          title: 'Bookings',
          value: stats.totalBookings.toString(),
          icon: Icons.calendar_today,
          color: Colors.purple,
        ),
        StatsCard(
          title: 'Total Spent',
          value: 'UGX ${stats.totalSpent.toStringAsFixed(2)}',
          icon: Icons.attach_money,
          color: AppTheme.accentOrange,
        ),
      ],
    );
  }
}

