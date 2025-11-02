import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:intl/intl.dart';

/// Recent recommendations list widget
class RecentRecommendationsList extends StatelessWidget {
  final List<RecommendationModel> recommendations;

  const RecentRecommendationsList({
    super.key,
    required this.recommendations,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Flexible(
                  child: Text(
                    'Recent Recommendations',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                TextButton(
                  onPressed: () {
                    context.push(AppRoutes.userRecommendations);
                  },
                  child: const Text('View All'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (recommendations.isEmpty)
              _buildEmptyState(context)
            else
              ...recommendations.map((rec) => _RecommendationCard(recommendation: rec)),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        children: [
          Icon(Icons.auto_awesome_outlined,
              size: 64, color: Colors.grey[300]),
          const SizedBox(height: 16),
          Text(
            'No recommendations yet',
            style: TextStyle(color: Colors.grey[600]),
          ),
          const SizedBox(height: 8),
          TextButton(
            onPressed: () {
              context.push('${AppRoutes.userRecommendations}/new');
            },
            child: const Text('Get Your First Recommendation'),
          ),
        ],
      ),
    );
  }
}

class _RecommendationCard extends StatelessWidget {
  final RecommendationModel recommendation;

  const _RecommendationCard({required this.recommendation});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: () {
          // Navigate to recommendations list page where user can see details
          context.push(AppRoutes.userRecommendations);
        },
        child: Padding(
          padding: const EdgeInsets.all(12),
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
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                  ),
                  if (recommendation.isSaved)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.blue.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Text(
                        'Saved',
                        style: TextStyle(
                          color: Colors.blue,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 8),
              if (recommendation.totalEstimatedCost != null &&
                  recommendation.totalEstimatedCost! > 0)
                Text(
                  'Estimated Cost: UGX ${recommendation.totalEstimatedCost!.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                    color: Colors.green,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                )
              else
                Text(
                  'Cost estimation pending',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontStyle: FontStyle.italic,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              if (recommendation.createdAt != null) ...[
                const SizedBox(height: 4),
                Text(
                  DateFormat('MMMM dd, yyyy').format(recommendation.createdAt!),
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
              const SizedBox(height: 8),
              TextButton(
                onPressed: () {
                  context.push(AppRoutes.userRecommendations);
                },
                style: TextButton.styleFrom(
                  padding: EdgeInsets.zero,
                  minimumSize: Size.zero,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text('View Details'),
                    SizedBox(width: 4),
                    Icon(Icons.arrow_forward, size: 16),
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

