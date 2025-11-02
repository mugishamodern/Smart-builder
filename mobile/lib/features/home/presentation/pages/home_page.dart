import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/features/auth/providers/auth_provider.dart';
import 'package:buildsmart_mobile/features/home/presentation/widgets/hero_section.dart';
import 'package:buildsmart_mobile/features/home/presentation/widgets/featured_section.dart';
import 'package:buildsmart_mobile/features/home/presentation/widgets/categories_grid.dart';
import 'package:buildsmart_mobile/features/home/providers/home_provider.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:go_router/go_router.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';

/// Home page - landing screen with hero section and featured content
/// 
/// Displays:
/// - Hero banner with CTAs
/// - Featured shops
/// - Featured products
/// - Featured services
/// - Category grid
class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(currentUserProvider);
    final user = authState.valueOrNull;

    return Scaffold(
      appBar: AppBar(
        title: const Text('BuildSmart'),
        backgroundColor: AppTheme.charcoalGray,
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {
              context.push(AppRoutes.search);
            },
            tooltip: 'Search',
          ),
          if (user != null)
            IconButton(
              icon: const Icon(Icons.account_circle),
              onPressed: () {
                context.push(AppRoutes.userDashboard);
              },
              tooltip: 'Profile',
            )
          else
            TextButton(
              onPressed: () {
                context.push(AppRoutes.login);
              },
              child: const Text(
                'Login',
                style: TextStyle(color: AppTheme.white),
              ),
            ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(featuredShopsProvider);
          ref.invalidate(featuredProductsProvider);
          ref.invalidate(featuredServicesProvider);
          ref.invalidate(categoriesProvider);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Hero Section
              const HeroSection(),
              
              const SizedBox(height: 24),
              
              // Featured Shops
              FeaturedSection<ShopModel>(
                title: 'Featured Shops',
                items: ref.watch(featuredShopsProvider),
                itemBuilder: (context, shop) => FeaturedShopCard(shop: shop),
              ),
              
              const SizedBox(height: 24),
              
              // Featured Products
              FeaturedSection<ProductModel>(
                title: 'Featured Products',
                items: ref.watch(featuredProductsProvider),
                itemBuilder: (context, product) =>
                    FeaturedProductCard(product: product),
              ),
              
              const SizedBox(height: 24),
              
              // Featured Services
              FeaturedSection<ServiceModel>(
                title: 'Featured Services',
                items: ref.watch(featuredServicesProvider),
                itemBuilder: (context, service) =>
                    FeaturedServiceCard(service: service),
              ),
              
              const SizedBox(height: 24),
              
              // Categories Grid
              const CategoriesGrid(),
              
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
      floatingActionButton: user?.isShopOwner == true
          ? FloatingActionButton.extended(
              onPressed: () {
                context.push(AppRoutes.shopDashboard);
              },
              backgroundColor: AppTheme.primaryYellow,
              foregroundColor: AppTheme.charcoalGray,
              icon: const Icon(Icons.dashboard),
              label: const Text('Shop Dashboard'),
            )
          : null,
    );
  }
}
