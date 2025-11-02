import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/user_dashboard/providers/user_dashboard_provider.dart';
import 'package:buildsmart_mobile/features/recommendations/providers/recommendation_provider.dart';
import 'package:intl/intl.dart';
import 'package:go_router/go_router.dart';

/// Recommendations list page
/// 
/// Displays user's saved recommendations with options to view, save, and delete
class RecommendationsListPage extends ConsumerWidget {
  const RecommendationsListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recommendationsState = ref.watch(
      userRecommendationsProvider(UserRecommendationsParams()),
    );
    final repository = ref.watch(recommendationRepositoryProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Recommendations'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => context.push(AppRoutes.userRecommendations),
            tooltip: 'New Recommendation',
          ),
        ],
      ),
      body: recommendationsState.when(
        data: (paginated) {
          if (paginated.recommendations.isEmpty) {
            return _buildEmptyState(context);
          }
          return RefreshIndicator(
            onRefresh: () async {
              ref.invalidate(
                userRecommendationsProvider(UserRecommendationsParams()),
              );
              await ref.read(
                userRecommendationsProvider(UserRecommendationsParams()).future,
              );
            },
            child: ListView.builder(
              itemCount: paginated.recommendations.length,
              padding: const EdgeInsets.all(16),
              itemBuilder: (context, index) {
                final rec = paginated.recommendations[index];
                return _RecommendationCard(
                  recommendation: rec,
                  onDelete: () async {
                    try {
                      await repository.deleteRecommendation(rec.id);
                      ref.invalidate(
                        userRecommendationsProvider(UserRecommendationsParams()),
                      );
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Recommendation deleted'),
                            backgroundColor: Colors.green,
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
                onPressed: () => ref.refresh(
                  userRecommendationsProvider(UserRecommendationsParams()),
                ),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push(AppRoutes.userRecommendations),
        icon: const Icon(Icons.auto_awesome),
        label: const Text('New Recommendation'),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.auto_awesome_outlined,
              size: 64, color: Colors.grey[300]),
          const SizedBox(height: 16),
          Text(
            'No recommendations yet',
            style: TextStyle(color: Colors.grey[600], fontSize: 18),
          ),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: () => context.push(AppRoutes.userRecommendations),
            icon: const Icon(Icons.add),
            label: const Text('Generate Recommendation'),
          ),
        ],
      ),
    );
  }
}

class _RecommendationCard extends StatelessWidget {
  final RecommendationModel recommendation;
  final VoidCallback onDelete;

  const _RecommendationCard({
    required this.recommendation,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: () {
          // TODO: Navigate to recommendation detail
          // context.push('${AppRoutes.userRecommendations}/${recommendation.id}');
        },
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      recommendation.projectType
                          .replaceAll('_', ' ')
                          .split(' ')
                          .map((word) => word.isEmpty
                              ? ''
                              : word[0].toUpperCase() + word.substring(1))
                          .join(' '),
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  if (recommendation.isSaved)
                    const Icon(Icons.bookmark, color: Colors.blue),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                recommendation.projectDescription,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[600]),
              ),
              const SizedBox(height: 8),
              if (recommendation.totalEstimatedCost != null &&
                  recommendation.totalEstimatedCost! > 0)
                Text(
                  'Estimated Cost: UGX ${recommendation.totalEstimatedCost!.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                )
              else
                Text(
                  'Cost estimation pending',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontStyle: FontStyle.italic,
                  ),
                ),
              if (recommendation.createdAt != null) ...[
                const SizedBox(height: 4),
                Text(
                  DateFormat('MMMM dd, yyyy').format(recommendation.createdAt!),
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () {
                      // Navigate to recommendation results if available
                      // For now, show a message
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Recommendation details view coming soon'),
                          duration: Duration(seconds: 2),
                        ),
                      );
                    },
                    child: const Text('View Details'),
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete_outline),
                    onPressed: () async {
                      final confirm = await showDialog<bool>(
                        context: context,
                        builder: (context) => AlertDialog(
                          title: const Text('Delete Recommendation'),
                          content: const Text(
                            'Are you sure you want to delete this recommendation?',
                          ),
                          actions: [
                            TextButton(
                              onPressed: () => Navigator.pop(context, false),
                              child: const Text('Cancel'),
                            ),
                            TextButton(
                              onPressed: () => Navigator.pop(context, true),
                              child: const Text('Delete'),
                            ),
                          ],
                        ),
                      );
                      if (confirm == true) {
                        onDelete();
                      }
                    },
                    color: Colors.red,
                    tooltip: 'Delete',
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

