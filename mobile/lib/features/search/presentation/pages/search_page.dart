import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/search/providers/search_provider.dart';
import 'package:buildsmart_mobile/features/search/presentation/widgets/search_filters_sheet.dart';
import 'package:buildsmart_mobile/features/search/presentation/widgets/search_results_list.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';

/// Search page with tabbed interface for products, shops, and services
class SearchPage extends ConsumerStatefulWidget {
  const SearchPage({super.key});

  @override
  ConsumerState<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends ConsumerState<SearchPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final TextEditingController _searchController = TextEditingController();
  final _debounceDelay = const Duration(milliseconds: 500);
  ProductSearchParams _productParams = ProductSearchParams();
  ServiceSearchParams _serviceParams = ServiceSearchParams();
  String? _shopQuery;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged(String value) {
    // Debounce search
    Future.delayed(_debounceDelay, () {
      if (!mounted || _searchController.text != value) return;

      setState(() {
        if (_tabController.index == 0) {
          // Products
          _productParams = _productParams.copyWith(query: value.isEmpty ? null : value);
        } else if (_tabController.index == 1) {
          // Shops
          _shopQuery = value.isEmpty ? null : value;
        } else {
          // Services
          _serviceParams = _serviceParams.copyWith(query: value.isEmpty ? null : value);
        }
      });
    });
  }

  void _showFilters() {
    if (_tabController.index == 0) {
      // Product filters
      showModalBottomSheet(
        context: context,
        isScrollControlled: true,
        backgroundColor: Colors.transparent,
        builder: (context) => SearchFiltersSheet(
          productParams: _productParams,
          onApply: (params) {
            setState(() {
              _productParams = params;
            });
          },
        ),
      );
    } else if (_tabController.index == 2) {
      // Service filters
      showModalBottomSheet(
        context: context,
        isScrollControlled: true,
        backgroundColor: Colors.transparent,
        builder: (context) => SearchFiltersSheet(
          serviceParams: _serviceParams,
          onApplyService: (params) {
            setState(() {
              _serviceParams = params;
            });
          },
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _searchController,
          decoration: const InputDecoration(
            hintText: 'Search products, shops, services...',
            border: InputBorder.none,
            hintStyle: TextStyle(color: Colors.white70),
          ),
          style: const TextStyle(color: Colors.white),
          onChanged: _onSearchChanged,
          autofocus: true,
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: _showFilters,
            tooltip: 'Filters',
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Products'),
            Tab(text: 'Shops'),
            Tab(text: 'Services'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // Products tab
          _productParams.query != null || _productParams.category != null
              ? ProductSearchResults(params: _productParams)
              : const Center(
                  child: Text('Start typing to search products'),
                ),

          // Shops tab
          _shopQuery != null
              ? ShopSearchResults(query: _shopQuery!)
              : const Center(
                  child: Text('Start typing to search shops'),
                ),

          // Services tab
          _serviceParams.query != null || _serviceParams.serviceType != null
              ? ServiceSearchResults(params: _serviceParams)
              : const Center(
                  child: Text('Start typing to search services'),
                ),
        ],
      ),
    );
  }
}

/// Product search results
class ProductSearchResults extends ConsumerWidget {
  final ProductSearchParams params;

  const ProductSearchResults({super.key, required this.params});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final searchState = ref.watch(productSearchProvider(params));
    final notifier = ref.read(productSearchProvider(params).notifier);

    return searchState.when(
      data: (result) {
        if (result.items.isEmpty) {
          return const Center(child: Text('No products found'));
        }
        return SearchResultsList<ProductModel>(
          items: result.items,
          hasMore: result.hasMore,
          onLoadMore: () => notifier.loadMore(),
          itemBuilder: (context, product) => _ProductCard(product: product),
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
              onPressed: () => ref.refresh(productSearchProvider(params)),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Shop search results
class ShopSearchResults extends ConsumerWidget {
  final String query;

  const ShopSearchResults({super.key, required this.query});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final searchState = ref.watch(shopSearchProvider(query));

    return searchState.when(
      data: (shops) {
        if (shops.isEmpty) {
          return const Center(child: Text('No shops found'));
        }
        return ListView.builder(
          itemCount: shops.length,
          itemBuilder: (context, index) {
            final shop = shops[index];
            return Card(
              margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: AppTheme.primaryYellow,
                  child: shop.name.isNotEmpty
                      ? Text(shop.name[0].toUpperCase())
                      : const Icon(Icons.store),
                ),
                title: Text(shop.name),
                subtitle: Text(shop.address),
                trailing: shop.isVerified
                    ? const Icon(Icons.verified, color: Colors.blue)
                    : null,
                onTap: () {
                  // Navigate to shop details
                  // TODO: Implement navigation
                },
              ),
            );
          },
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
              onPressed: () => ref.refresh(shopSearchProvider(query)),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Service search results
class ServiceSearchResults extends ConsumerWidget {
  final ServiceSearchParams params;

  const ServiceSearchResults({super.key, required this.params});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final searchState = ref.watch(serviceSearchProvider(params));
    final notifier = ref.read(serviceSearchProvider(params).notifier);

    return searchState.when(
      data: (result) {
        if (result.items.isEmpty) {
          return const Center(child: Text('No services found'));
        }
        return SearchResultsList<ServiceModel>(
          items: result.items,
          hasMore: result.hasMore,
          onLoadMore: () => notifier.loadMore(),
          itemBuilder: (context, service) => _ServiceCard(service: service),
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
              onPressed: () => ref.refresh(serviceSearchProvider(params)),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Product card widget
class _ProductCard extends StatelessWidget {
  final ProductModel product;

  const _ProductCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: () {
          // Navigate to product details
          // TODO: Implement navigation
        },
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Product image placeholder
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: product.imageUrl != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: Image.network(
                          product.imageUrl!,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) =>
                              const Icon(Icons.image),
                        ),
                      )
                    : const Icon(Icons.inventory_2),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      product.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    if (product.description != null)
                      Text(
                        product.description!,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Text(
                          'UGX ${product.price.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppTheme.accentOrange,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Chip(
                          label: Text(product.category),
                          labelStyle: const TextStyle(fontSize: 10),
                          padding: const EdgeInsets.all(2),
                        ),
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

/// Service card widget
class _ServiceCard extends StatelessWidget {
  final ServiceModel service;

  const _ServiceCard({required this.service});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: () {
          // Navigate to service details
          // TODO: Implement navigation
        },
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.build,
                    color: AppTheme.primaryYellow,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      service.title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              if (service.description != null) ...[
                const SizedBox(height: 8),
                Text(
                  service.description!,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: Colors.grey[600]),
                ),
              ],
              const SizedBox(height: 8),
              Row(
                children: [
                  Text(
                    'UGX ${service.hourlyRate.toStringAsFixed(2)}/hr',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.accentOrange,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Chip(
                    label: Text(service.serviceType),
                    labelStyle: const TextStyle(fontSize: 10),
                    padding: const EdgeInsets.all(2),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

