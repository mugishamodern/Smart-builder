import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/search/providers/search_provider.dart';
import 'package:buildsmart_mobile/features/services/presentation/widgets/service_card.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';

/// Services list page
/// 
/// Displays available services with filtering options
class ServicesListPage extends ConsumerStatefulWidget {
  const ServicesListPage({super.key});

  @override
  ConsumerState<ServicesListPage> createState() => _ServicesListPageState();
}

class _ServicesListPageState extends ConsumerState<ServicesListPage> {
  String? _selectedServiceType;
  bool _showFilters = false;

  @override
  Widget build(BuildContext context) {
    final searchParams = ServiceSearchParams(
      serviceType: _selectedServiceType,
    );
    final servicesState = ref.watch(serviceSearchProvider(searchParams));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Services'),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: () {
              setState(() => _showFilters = !_showFilters);
            },
            tooltip: 'Filters',
          ),
        ],
      ),
      body: Column(
        children: [
          // Filters
          if (_showFilters)
            Card(
              margin: EdgeInsets.zero,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Filter by Service Type',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        _FilterChip(
                          label: 'All',
                          selected: _selectedServiceType == null,
                          onSelected: (value) {
                            setState(() => _selectedServiceType = null);
                          },
                        ),
                        _FilterChip(
                          label: 'Plumbing',
                          selected: _selectedServiceType == 'plumbing',
                          onSelected: (value) {
                            setState(() => _selectedServiceType = 'plumbing');
                          },
                        ),
                        _FilterChip(
                          label: 'Electrical',
                          selected: _selectedServiceType == 'electrical',
                          onSelected: (value) {
                            setState(() => _selectedServiceType = 'electrical');
                          },
                        ),
                        _FilterChip(
                          label: 'Carpentry',
                          selected: _selectedServiceType == 'carpentry',
                          onSelected: (value) {
                            setState(() => _selectedServiceType = 'carpentry');
                          },
                        ),
                        _FilterChip(
                          label: 'Masonry',
                          selected: _selectedServiceType == 'masonry',
                          onSelected: (value) {
                            setState(() => _selectedServiceType = 'masonry');
                          },
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          // Services list
          Expanded(
            child: servicesState.when(
              data: (result) {
                if (result.items.isEmpty) {
                  return const Center(child: Text('No services found'));
                }
                return RefreshIndicator(
                  onRefresh: () async {
                    ref.invalidate(serviceSearchProvider(searchParams));
                    await Future.delayed(const Duration(milliseconds: 100));
                  },
                  child: ListView.builder(
                    itemCount: result.items.length,
                    padding: const EdgeInsets.all(16),
                    itemBuilder: (context, index) {
                      final service = result.items[index];
                      return ServiceCard(
                        service: service,
                        onTap: () {
                          // Service detail page not yet implemented
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Service detail page coming soon'),
                              duration: Duration(seconds: 2),
                            ),
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
                    const Icon(Icons.error_outline,
                        size: 48, color: Colors.red),
                    const SizedBox(height: 16),
                    Text('Error: ${err.toString()}'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () =>
                          ref.refresh(serviceSearchProvider(searchParams)),
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final Function(bool) onSelected;

  const _FilterChip({
    required this.label,
    required this.selected,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Text(label),
      selected: selected,
      onSelected: onSelected,
      selectedColor: AppTheme.primaryYellow.withValues(alpha: 0.3),
    );
  }
}

