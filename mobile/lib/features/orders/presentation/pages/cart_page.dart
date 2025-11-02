import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/orders/providers/cart_provider.dart';
import 'package:buildsmart_mobile/features/orders/presentation/widgets/cart_item_widget.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:go_router/go_router.dart';

/// Cart page
/// 
/// Displays shopping cart with items, quantities, and checkout button
class CartPage extends ConsumerWidget {
  const CartPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cartState = ref.watch(cartProvider);
    final cartNotifier = ref.watch(cartNotifierProvider.notifier);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Shopping Cart'),
        actions: [
          if (cartState.valueOrNull?.isNotEmpty == true)
            IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: () async {
                final confirm = await showDialog<bool>(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('Clear Cart'),
                    content: const Text('Are you sure you want to clear all items from your cart?'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context, false),
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () => Navigator.pop(context, true),
                        child: const Text('Clear'),
                      ),
                    ],
                  ),
                );
                if (confirm == true) {
                  await cartNotifier.clear();
                }
              },
              tooltip: 'Clear Cart',
            ),
        ],
      ),
      body: cartState.when(
        data: (cart) {
          if (cart.isEmpty) {
            return _buildEmptyState(context);
          }
          return Column(
            children: [
              Expanded(
                child: RefreshIndicator(
                  onRefresh: () => cartNotifier.refresh(),
                  child: ListView.builder(
                    itemCount: cart.items.length,
                    padding: const EdgeInsets.all(16),
                    itemBuilder: (context, index) {
                      final item = cart.items[index];
                      return CartItemWidget(
                        item: item,
                        onUpdateQuantity: (quantity) {
                          cartNotifier.updateQuantity(item.id, quantity);
                        },
                        onRemove: () {
                          cartNotifier.removeItem(item.id);
                        },
                      );
                    },
                  ),
                ),
              ),
              _buildCartSummary(context, cart),
            ],
          );
        },
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
                onPressed: () => cartNotifier.refresh(),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.shopping_cart_outlined,
              size: 64, color: Colors.grey[300]),
          const SizedBox(height: 16),
          Text(
            'Your cart is empty',
            style: TextStyle(color: Colors.grey[600], fontSize: 18),
          ),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: () => context.push(AppRoutes.search),
            child: const Text('Browse Products'),
          ),
        ],
      ),
    );
  }

  Widget _buildCartSummary(BuildContext context, cart) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 4,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Total',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                'UGX ${cart.total.toStringAsFixed(2)}',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.accentOrange,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () => context.push(AppRoutes.checkout),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: AppTheme.accentOrange,
              ),
              child: const Text(
                'Proceed to Checkout',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

