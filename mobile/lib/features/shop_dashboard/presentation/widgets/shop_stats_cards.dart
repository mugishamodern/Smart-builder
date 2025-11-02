import 'package:flutter/material.dart';
import 'package:buildsmart_mobile/features/shop_dashboard/data/repositories/shop_dashboard_repository.dart';

/// Shop statistics cards widget
class ShopStatsCards extends StatelessWidget {
  final ShopDashboardStats stats;

  const ShopStatsCards({super.key, required this.stats});

  @override
  Widget build(BuildContext context) {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      childAspectRatio: 1.3,
      children: [
        _StatCard(
          title: 'Total Products',
          value: stats.totalProducts.toString(),
          icon: Icons.inventory_2,
          color: Colors.blue,
        ),
        _StatCard(
          title: 'Total Sales',
          value: 'UGX ${stats.totalSales.toStringAsFixed(2)}',
          icon: Icons.attach_money,
          color: Colors.green,
        ),
        _StatCard(
          title: 'Avg Rating',
          value: stats.avgRating.toStringAsFixed(2),
          icon: Icons.star,
          color: Colors.amber,
        ),
        _StatCard(
          title: 'Customers',
          value: stats.totalCustomers.toString(),
          icon: Icons.people,
          color: Colors.purple,
        ),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: color,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Icon(icon, color: Colors.white, size: 24),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 12,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
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

