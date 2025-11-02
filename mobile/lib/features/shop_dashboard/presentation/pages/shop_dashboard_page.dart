import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/data/repositories/shop_dashboard_repository.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/providers/shop_dashboard_provider.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/presentation/widgets/shop_card.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/presentation/widgets/shop_stats_cards.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/presentation/widgets/shop_recent_orders_list.dart';

/// Shop dashboard page
/// 
/// Displays shop owner's shops, statistics, and recent orders
class ShopDashboardPage extends ConsumerWidget {
  const ShopDashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboardData = ref.watch(shopDashboardDataProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Shop Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {
              // Shop registration page not yet implemented
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Shop registration feature coming soon'),
                  duration: Duration(seconds: 2),
                ),
              );
            },
            tooltip: 'Register New Shop',
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(shopDashboardDataProvider);
          await ref.read(shopDashboardDataProvider.future);
        },
        child: dashboardData.when(
          data: (data) => _buildDashboardContent(context, data),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) => Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: Colors.red),
                const SizedBox(height: 16),
                Text('Error: ${err.toString()}'),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () => ref.refresh(shopDashboardDataProvider),
                  child: const Text('Retry'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDashboardContent(BuildContext context, ShopDashboardData data) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome header
          const Text(
            'My Shops',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),

          // Shops list
          if (data.shops.isEmpty)
            _buildEmptyShopsState(context)
          else
            ...data.shops.map((shop) => ShopCard(shop: shop)),

          const SizedBox(height: 32),

          // Analytics section
          const Text(
            'Analytics',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          ShopStatsCards(stats: data.stats),

          const SizedBox(height: 32),

          // Recent orders
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Recent Orders',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              TextButton(
                onPressed: () {
                  // Orders list view not yet implemented
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Orders list view coming soon'),
                      duration: Duration(seconds: 2),
                    ),
                  );
                },
                child: const Text('View All'),
              ),
            ],
          ),
          const SizedBox(height: 16),
          ShopRecentOrdersList(orders: data.recentOrders),
        ],
      ),
    );
  }

  Widget _buildEmptyShopsState(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          children: [
            Icon(Icons.store_outlined, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text(
              'You do not own any shops yet',
              style: TextStyle(color: Colors.grey[600]),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: () {
                // Shop registration page not yet implemented
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Shop registration feature coming soon'),
                    duration: Duration(seconds: 2),
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Register a Shop'),
            ),
          ],
        ),
      ),
    );
  }
}

