import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/inventory/providers/inventory_provider.dart';
import 'package:buildsmart_mobile/features/inventory/presentation/widgets/product_list_item.dart';
import 'package:buildsmart_mobile/features/inventory/presentation/pages/add_edit_product_page.dart';
import 'package:go_router/go_router.dart';

/// Inventory management page
/// 
/// Displays list of products for a shop with options to add/edit/delete
class InventoryPage extends ConsumerWidget {
  final int shopId;

  const InventoryPage({super.key, required this.shopId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final inventory = ref.watch(shopInventoryProvider(shopId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Inventory'),
      ),
      body: inventory.when(
        data: (products) {
          if (products.isEmpty) {
            return _buildEmptyState(context);
          }
          return RefreshIndicator(
            onRefresh: () async {
              ref.invalidate(shopInventoryProvider(shopId));
              await ref.read(shopInventoryProvider(shopId).future);
            },
            child: ListView.builder(
              itemCount: products.length,
              padding: const EdgeInsets.all(16),
              itemBuilder: (context, index) {
                final product = products[index];
                return ProductListItem(
                  product: product,
                  shopId: shopId,
                  onEdit: () {
                    context.push(
                      '${AddEditProductPage.route}/$shopId/${product.id}',
                    );
                  },
                );
              },
            ),
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
                onPressed: () => ref.refresh(shopInventoryProvider(shopId)),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          context.push('${AddEditProductPage.route}/$shopId');
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.inventory_2_outlined, size: 64, color: Colors.grey[300]),
          const SizedBox(height: 16),
          Text(
            'No products yet',
            style: TextStyle(color: Colors.grey[600]),
          ),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: () {
              context.push('${AddEditProductPage.route}/$shopId');
            },
            icon: const Icon(Icons.add),
            label: const Text('Add Product'),
          ),
        ],
      ),
    );
  }
}

