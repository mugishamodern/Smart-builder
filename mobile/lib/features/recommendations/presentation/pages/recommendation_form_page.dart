import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/routing/routes.dart';
import 'package:buildsmart_mobile/features/recommendations/providers/recommendation_provider.dart';
import 'package:go_router/go_router.dart';

/// Recommendation form page
/// 
/// Form for submitting project details to generate AI recommendations
class RecommendationFormPage extends ConsumerStatefulWidget {
  const RecommendationFormPage({super.key});

  @override
  ConsumerState<RecommendationFormPage> createState() =>
      _RecommendationFormPageState();
}

class _RecommendationFormPageState
    extends ConsumerState<RecommendationFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _descriptionController = TextEditingController();
  String _projectType = '2_bedroom_house';
  bool _isLoading = false;

  final List<String> _projectTypes = [
    '2_bedroom_house',
    '3_bedroom_house',
    '4_bedroom_house',
    'office_building',
    'commercial_space',
    'renovation',
    'custom',
  ];

  @override
  void dispose() {
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _generateRecommendation() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final notifier = ref.read(recommendationGenerationProvider.notifier);
      await notifier.generateRecommendation(
        projectDescription: _descriptionController.text.trim(),
        projectType: _projectType,
      );

      if (mounted) {
        context.push(AppRoutes.userRecommendations);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Recommendation'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Info card
              Card(
                color: Colors.blue.withValues(alpha: 0.1),
                child: const Padding(
                  padding: EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Icon(Icons.auto_awesome, color: Colors.blue),
                      SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'Describe your construction project and get AI-powered recommendations for materials, services, and costs.',
                          style: TextStyle(fontSize: 14),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Project type
              const Text(
                'Project Type',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                initialValue: _projectType,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                ),
                items: _projectTypes.map((type) {
                  return DropdownMenuItem(
                    value: type,
                    child: Text(
                      type
                          .replaceAll('_', ' ')
                          .split(' ')
                          .map((word) => word.isEmpty
                              ? ''
                              : word[0].toUpperCase() + word.substring(1))
                          .join(' '),
                    ),
                  );
                }).toList(),
                onChanged: (value) => setState(() => _projectType = value!),
              ),
              const SizedBox(height: 24),

              // Project description
              const Text(
                'Project Description *',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText:
                      'Describe your construction project in detail...\n\nExample: Building a 3-bedroom house with 2 bathrooms, kitchen, living room, and a carport. Need modern finishes and quality materials.',
                ),
                maxLines: 8,
                validator: (value) => value?.isEmpty ?? true
                    ? 'Project description is required'
                    : null,
              ),
              const SizedBox(height: 32),

              // Generate button
              ElevatedButton(
                onPressed: _isLoading ? null : _generateRecommendation,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.auto_awesome),
                          SizedBox(width: 8),
                          Text(
                            'Generate Recommendation',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
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

