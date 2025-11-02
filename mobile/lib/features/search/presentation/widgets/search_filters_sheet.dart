import 'package:flutter/material.dart';
import 'package:buildsmart_mobile/features/search/providers/search_provider.dart';

/// Bottom sheet for search filters
class SearchFiltersSheet extends StatefulWidget {
  final ProductSearchParams? productParams;
  final ServiceSearchParams? serviceParams;
  final void Function(ProductSearchParams)? onApply;
  final void Function(ServiceSearchParams)? onApplyService;

  const SearchFiltersSheet({
    super.key,
    this.productParams,
    this.serviceParams,
    this.onApply,
    this.onApplyService,
  }) : assert(
          (productParams != null && onApply != null) ||
              (serviceParams != null && onApplyService != null),
          'Either product or service params must be provided',
        );

  @override
  State<SearchFiltersSheet> createState() => _SearchFiltersSheetState();
}

class _SearchFiltersSheetState extends State<SearchFiltersSheet> {
  late final TextEditingController _minPriceController;
  late final TextEditingController _maxPriceController;
  late final TextEditingController _categoryController;
  String? _selectedCategory;

  // Service-specific
  late final TextEditingController _minRateController;
  late final TextEditingController _maxRateController;
  late final TextEditingController _serviceTypeController;
  String? _selectedServiceType;

  @override
  void initState() {
    super.initState();
    if (widget.productParams != null) {
      _minPriceController = TextEditingController(
        text: widget.productParams!.minPrice?.toString() ?? '',
      );
      _maxPriceController = TextEditingController(
        text: widget.productParams!.maxPrice?.toString() ?? '',
      );
      _categoryController = TextEditingController(
        text: widget.productParams!.category ?? '',
      );
      _selectedCategory = widget.productParams!.category;
    } else {
      _minPriceController = TextEditingController();
      _maxPriceController = TextEditingController();
      _categoryController = TextEditingController();
    }

    if (widget.serviceParams != null) {
      _minRateController = TextEditingController(
        text: widget.serviceParams!.minRate?.toString() ?? '',
      );
      _maxRateController = TextEditingController(
        text: widget.serviceParams!.maxRate?.toString() ?? '',
      );
      _serviceTypeController = TextEditingController(
        text: widget.serviceParams!.serviceType ?? '',
      );
      _selectedServiceType = widget.serviceParams!.serviceType;
    } else {
      _minRateController = TextEditingController();
      _maxRateController = TextEditingController();
      _serviceTypeController = TextEditingController();
    }
  }

  @override
  void dispose() {
    _minPriceController.dispose();
    _maxPriceController.dispose();
    _categoryController.dispose();
    _minRateController.dispose();
    _maxRateController.dispose();
    _serviceTypeController.dispose();
    super.dispose();
  }

  void _applyFilters() {
    if (widget.productParams != null) {
      final params = ProductSearchParams(
        query: widget.productParams!.query,
        category: _selectedCategory,
        minPrice: _minPriceController.text.isEmpty
            ? null
            : double.tryParse(_minPriceController.text),
        maxPrice: _maxPriceController.text.isEmpty
            ? null
            : double.tryParse(_maxPriceController.text),
        page: 1,
      );
      widget.onApply?.call(params);
    } else if (widget.serviceParams != null) {
      final params = ServiceSearchParams(
        query: widget.serviceParams!.query,
        serviceType: _selectedServiceType,
        minRate: _minRateController.text.isEmpty
            ? null
            : double.tryParse(_minRateController.text),
        maxRate: _maxRateController.text.isEmpty
            ? null
            : double.tryParse(_maxRateController.text),
        page: 1,
      );
      widget.onApplyService?.call(params);
    }
    Navigator.pop(context);
  }

  void _clearFilters() {
    setState(() {
      _minPriceController.clear();
      _maxPriceController.clear();
      _categoryController.clear();
      _selectedCategory = null;
      _minRateController.clear();
      _maxRateController.clear();
      _serviceTypeController.clear();
      _selectedServiceType = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    final isProductFilters = widget.productParams != null;

    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: DraggableScrollableSheet(
        initialChildSize: 0.6,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        builder: (context, scrollController) {
          return Column(
            children: [
              // Handle bar
              Container(
                margin: const EdgeInsets.symmetric(vertical: 12),
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              // Title and actions
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Filters',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    TextButton(
                      onPressed: _clearFilters,
                      child: const Text('Clear'),
                    ),
                  ],
                ),
              ),
              const Divider(),
              // Filter content
              Expanded(
                child: ListView(
                  controller: scrollController,
                  padding: const EdgeInsets.all(16),
                  children: isProductFilters
                      ? _buildProductFilters()
                      : _buildServiceFilters(),
                ),
              ),
              // Apply button
              Container(
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
                child: SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _applyFilters,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Apply Filters'),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  List<Widget> _buildProductFilters() {
    return [
      // Category
      const Text(
        'Category',
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 8),
      TextField(
        controller: _categoryController,
        decoration: const InputDecoration(
          hintText: 'e.g., Cement, Steel, Tools',
          border: OutlineInputBorder(),
        ),
        onChanged: (value) => setState(() => _selectedCategory = value),
      ),
      const SizedBox(height: 24),

      // Price range
      const Text(
        'Price Range',
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 8),
      Row(
        children: [
          Expanded(
            child: TextField(
              controller: _minPriceController,
              decoration: const InputDecoration(
                labelText: 'Min Price',
                border: OutlineInputBorder(),
                prefixText: 'UGX ',
              ),
              keyboardType: TextInputType.number,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: TextField(
              controller: _maxPriceController,
              decoration: const InputDecoration(
                labelText: 'Max Price',
                border: OutlineInputBorder(),
                prefixText: 'UGX ',
              ),
              keyboardType: TextInputType.number,
            ),
          ),
        ],
      ),
    ];
  }

  List<Widget> _buildServiceFilters() {
    return [
      // Service type
      const Text(
        'Service Type',
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 8),
      TextField(
        controller: _serviceTypeController,
        decoration: const InputDecoration(
          hintText: 'e.g., Engineering, Design, Consulting',
          border: OutlineInputBorder(),
        ),
        onChanged: (value) => setState(() => _selectedServiceType = value),
      ),
      const SizedBox(height: 24),

      // Rate range
      const Text(
        'Hourly Rate Range',
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 8),
      Row(
        children: [
          Expanded(
            child: TextField(
              controller: _minRateController,
              decoration: const InputDecoration(
                labelText: 'Min Rate',
                border: OutlineInputBorder(),
                prefixText: 'UGX ',
                suffixText: '/hr',
              ),
              keyboardType: TextInputType.number,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: TextField(
              controller: _maxRateController,
              decoration: const InputDecoration(
                labelText: 'Max Rate',
                border: OutlineInputBorder(),
                prefixText: 'UGX ',
                suffixText: '/hr',
              ),
              keyboardType: TextInputType.number,
            ),
          ),
        ],
      ),
    ];
  }
}

