import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/orders/providers/cart_provider.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';

/// Featured section widget
/// 
/// Displays a horizontal scrollable list of featured items
class FeaturedSection<T> extends ConsumerWidget {
  final String title;
  final AsyncValue<List<T>> items;
  final Widget Function(BuildContext, T) itemBuilder;

  const FeaturedSection({
    super.key,
    required this.title,
    required this.items,
    required this.itemBuilder,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              TextButton(
                onPressed: () {
                  context.push(AppRoutes.search);
                },
                child: const Text('See All'),
              ),
            ],
          ),
        ),
        items.when(
          data: (itemsList) {
            if (itemsList.isEmpty) {
              return const SizedBox(
                height: 120,
                child: Center(
                  child: Text('No items available'),
                ),
              );
            }

            return SizedBox(
              height: 200,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                itemCount: itemsList.length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 12.0),
                    child: itemBuilder(context, itemsList[index]),
                  );
                },
              ),
            );
          },
          loading: () => const SizedBox(
            height: 200,
            child: Center(
              child: CircularProgressIndicator(),
            ),
          ),
          error: (error, stack) => SizedBox(
            height: 200,
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.red),
                  const SizedBox(height: 8),
                  Text(
                    'Failed to load $title',
                    style: const TextStyle(color: Colors.red),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Featured shop card
class FeaturedShopCard extends StatelessWidget {
  final ShopModel shop;

  const FeaturedShopCard({super.key, required this.shop});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.push(
          '${AppRoutes.shopDetail.replaceAll(':id', '${shop.id}')}',
        );
      },
      child: SizedBox(
        width: 160,
        child: Card(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                height: 100,
                decoration: BoxDecoration(
                  color: AppTheme.bgLight,
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(12),
                  ),
                ),
                child: Center(
                  child: Icon(
                    Icons.store,
                    size: 48,
                    color: AppTheme.primaryYellow,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(12.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      shop.name,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 4),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.star,
                          size: 14,
                          color: AppTheme.primaryYellow,
                        ),
                        const SizedBox(width: 4),
                        Flexible(
                          child: Text(
                            shop.rating.toStringAsFixed(1),
                            style: const TextStyle(fontSize: 12),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        if (shop.isVerified) ...[
                          const SizedBox(width: 4),
                          Icon(
                            Icons.verified,
                            size: 14,
                            color: AppTheme.accentOrange,
                          ),
                        ],
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// Featured product card
class FeaturedProductCard extends ConsumerWidget {
  final ProductModel product;

  const FeaturedProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return SizedBox(
      width: 160,
      child: Card(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Stack(
              children: [
                GestureDetector(
                  onTap: () {
                    context.push(
                      '${AppRoutes.productDetail.replaceAll(':id', '${product.id}')}',
                    );
                  },
                  child: Container(
                    height: 90,
                    decoration: BoxDecoration(
                      color: AppTheme.bgLight,
                      borderRadius: const BorderRadius.vertical(
                        top: Radius.circular(12),
                      ),
                    ),
                    child: product.imageUrl != null
                        ? ClipRRect(
                            borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(12),
                            ),
                            child: Image.network(
                              product.imageUrl!,
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) =>
                                  _buildPlaceholder(),
                            ),
                          )
                        : _buildPlaceholder(),
                  ),
                ),
                // Add to Cart icon button
                if (product.isAvailable && product.quantityAvailable > 0)
                  Positioned(
                    top: 4,
                    right: 4,
                    child: Material(
                      color: AppTheme.primaryYellow,
                      borderRadius: BorderRadius.circular(20),
                      child: InkWell(
                        onTap: () async {
                          final cartNotifier = ref.read(cartNotifierProvider.notifier);
                          try {
                            await cartNotifier.addToCart(product.id, 1);
                            if (context.mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('${product.name} added to cart'),
                                  backgroundColor: Colors.green,
                                  duration: const Duration(seconds: 2),
                                ),
                              );
                            }
                          } catch (e) {
                            if (context.mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Error: ${e.toString()}'),
                                  backgroundColor: Colors.red,
                                ),
                              );
                            }
                          }
                        },
                        borderRadius: BorderRadius.circular(20),
                        child: const Padding(
                          padding: EdgeInsets.all(6),
                          child: Icon(
                            Icons.add_shopping_cart,
                            size: 16,
                            color: AppTheme.charcoalGray,
                          ),
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            Flexible(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    GestureDetector(
                      onTap: () {
                        context.push(
                          '${AppRoutes.productDetail.replaceAll(':id', '${product.id}')}',
                        );
                      },
                      child: Text(
                        product.name,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      'UGX ${product.price.toStringAsFixed(2)}/${product.unit}',
                      style: TextStyle(
                        color: AppTheme.primaryYellow,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      product.category,
                      style: TextStyle(
                        fontSize: 10,
                        color: AppTheme.gray500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaceholder() {
    return Center(
      child: Icon(
        Icons.inventory_2,
        size: 48,
        color: AppTheme.gray500,
      ),
    );
  }
}

/// Featured service card
class FeaturedServiceCard extends StatelessWidget {
  final ServiceModel service;

  const FeaturedServiceCard({super.key, required this.service});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.push(
          '${AppRoutes.serviceDetail.replaceAll(':id', '${service.id}')}',
        );
      },
      child: SizedBox(
        width: 160,
        child: Card(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                height: 90,
                decoration: BoxDecoration(
                  color: AppTheme.bgLight,
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(12),
                  ),
                ),
                child: Center(
                  child: Icon(
                    _getServiceIcon(service.serviceType),
                    size: 40,
                    color: AppTheme.accentOrange,
                  ),
                ),
              ),
              Flexible(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        service.title,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        'UGX ${service.hourlyRate.toStringAsFixed(2)}/hr',
                        style: TextStyle(
                          color: AppTheme.accentOrange,
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.star,
                            size: 12,
                            color: AppTheme.primaryYellow,
                          ),
                          const SizedBox(width: 3),
                          Flexible(
                            child: Text(
                              service.rating.toStringAsFixed(1),
                              style: const TextStyle(fontSize: 10),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getServiceIcon(String serviceType) {
    switch (serviceType.toLowerCase()) {
      case 'plumbing':
        return Icons.plumbing;
      case 'electrical':
        return Icons.electrical_services;
      case 'carpentry':
        return Icons.carpenter;
      default:
        return Icons.build;
    }
  }
}
