import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/recommendations/providers/recommendation_provider.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:go_router/go_router.dart';

/// Recommendation results page
/// 
/// Displays AI-generated recommendation results with materials, costs, and services
class RecommendationResultsPage extends ConsumerWidget {
  const RecommendationResultsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recommendationState = ref.watch(recommendationGenerationProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Recommendation Results'),
        actions: [
          if (recommendationState.valueOrNull != null)
            IconButton(
              icon: const Icon(Icons.save),
              onPressed: () {
                // TODO: Implement save functionality
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Save feature coming soon'),
                  ),
                );
              },
              tooltip: 'Save Recommendation',
            ),
        ],
      ),
      body: recommendationState.when(
        data: (recommendation) {
          if (recommendation == null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.auto_awesome_outlined, size: 64),
                  const SizedBox(height: 16),
                  const Text('No recommendation generated yet'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => context.push(AppRoutes.userRecommendations),
                    child: const Text('Generate Recommendation'),
                  ),
                ],
              ),
            );
          }
          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Cost estimate card
                Card(
                  color: AppTheme.accentOrange.withValues(alpha: 0.1),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        const Text(
                          'Estimated Total Cost',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'UGX ${recommendation.costEstimate.total.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: AppTheme.accentOrange,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Confidence: ${(recommendation.confidenceScore * 100).toStringAsFixed(0)}%',
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Materials section
                const Text(
                  'Recommended Materials',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                ...recommendation.materials.map(
                  (material) => Card(
                    margin: const EdgeInsets.only(bottom: 8),
                    child: ListTile(
                      leading: const Icon(Icons.inventory_2),
                      title: Text(material.name),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('${material.quantity} ${material.unit}'),
                          if (material.description != null)
                            Text(material.description!),
                          Text(
                            material.category,
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Services section
                if (recommendation.services.isNotEmpty) ...[
                  const Text(
                    'Recommended Services',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  ...recommendation.services.map(
                    (service) => Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: const Icon(Icons.build),
                        title: Text(service.serviceType),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(service.description),
                            if (service.estimatedCost != null)
                              Text(
                                'Estimated: UGX ${service.estimatedCost!.toStringAsFixed(2)}',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.accentOrange,
                                ),
                              ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],

                // Shopping plan
                if (recommendation.shoppingPlan.isNotEmpty) ...[
                  const Text(
                    'Shopping Plan',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  ...recommendation.shoppingPlan.map(
                    (plan) => Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: const Icon(Icons.store),
                        title: Text(plan.shopName),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('${plan.distance.toStringAsFixed(1)} km away'),
                            const SizedBox(height: 4),
                            Text(
                              'Materials: ${plan.materials.join(', ')}',
                              style: TextStyle(fontSize: 12),
                            ),
                            Text(
                              'Est. Cost: UGX ${plan.estimatedCost.toStringAsFixed(2)}',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: AppTheme.accentOrange,
                              ),
                            ),
                          ],
                        ),
                        trailing: TextButton(
                          onPressed: () {
                            // Shop detail page not yet implemented
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Shop detail page coming soon'),
                                duration: Duration(seconds: 2),
                              ),
                            );
                          },
                          child: const Text('View Shop'),
                        ),
                      ),
                    ),
                  ),
                ],
              ],
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
                onPressed: () => context.push(AppRoutes.userRecommendations),
                child: const Text('Try Again'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

