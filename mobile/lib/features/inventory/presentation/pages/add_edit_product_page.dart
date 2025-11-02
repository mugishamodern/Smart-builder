import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/features/inventory/providers/inventory_provider.dart';
import 'package:go_router/go_router.dart';

/// Add/Edit product page
/// 
/// Form for adding new products or editing existing ones
class AddEditProductPage extends ConsumerStatefulWidget {
  static const String route = '/inventory/shop';

  final int shopId;
  final int? productId; // null for add, non-null for edit

  const AddEditProductPage({
    super.key,
    required this.shopId,
    this.productId,
  });

  @override
  ConsumerState<AddEditProductPage> createState() =>
      _AddEditProductPageState();
}

class _AddEditProductPageState extends ConsumerState<AddEditProductPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _categoryController = TextEditingController();
  final _priceController = TextEditingController();
  final _unitController = TextEditingController();
  final _quantityController = TextEditingController();
  final _minOrderController = TextEditingController();
  final _brandController = TextEditingController();
  final _imageUrlController = TextEditingController();

  bool _isAvailable = true;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.productId != null) {
      // Load existing product data
      _loadProduct();
    } else {
      _quantityController.text = '0';
      _minOrderController.text = '1';
    }
  }

  void _loadProduct() {
    final inventory = ref.read(shopInventoryProvider(widget.shopId));
    inventory.whenData((products) {
      final product = products.firstWhere(
        (p) => p.id == widget.productId,
      );
      _nameController.text = product.name;
      _descriptionController.text = product.description ?? '';
      _categoryController.text = product.category;
      _priceController.text = product.price.toString();
      _unitController.text = product.unit;
      _quantityController.text = product.quantityAvailable.toString();
      _minOrderController.text = product.minOrderQuantity.toString();
      _brandController.text = product.brand ?? '';
      _imageUrlController.text = product.imageUrl ?? '';
      _isAvailable = product.isAvailable;
    });
  }

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _categoryController.dispose();
    _priceController.dispose();
    _unitController.dispose();
    _quantityController.dispose();
    _minOrderController.dispose();
    _brandController.dispose();
    _imageUrlController.dispose();
    super.dispose();
  }

  Future<void> _saveProduct() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final repository = ref.read(inventoryRepositoryProvider);

      if (widget.productId == null) {
        // Add new product
        await repository.addProduct(
          shopId: widget.shopId,
          name: _nameController.text.trim(),
          description: _descriptionController.text.trim().isEmpty
              ? null
              : _descriptionController.text.trim(),
          category: _categoryController.text.trim(),
          price: double.parse(_priceController.text),
          unit: _unitController.text.trim(),
          quantityAvailable: int.parse(_quantityController.text),
          minOrderQuantity: int.parse(_minOrderController.text),
          isAvailable: _isAvailable,
          brand: _brandController.text.trim().isEmpty
              ? null
              : _brandController.text.trim(),
          imageUrl: _imageUrlController.text.trim().isEmpty
              ? null
              : _imageUrlController.text.trim(),
        );
      } else {
        // Update existing product
        await repository.updateProduct(
          shopId: widget.shopId,
          productId: widget.productId!,
          name: _nameController.text.trim(),
          description: _descriptionController.text.trim().isEmpty
              ? null
              : _descriptionController.text.trim(),
          category: _categoryController.text.trim(),
          price: double.tryParse(_priceController.text),
          unit: _unitController.text.trim(),
          quantityAvailable: int.tryParse(_quantityController.text),
          minOrderQuantity: int.tryParse(_minOrderController.text),
          isAvailable: _isAvailable,
          brand: _brandController.text.trim().isEmpty
              ? null
              : _brandController.text.trim(),
          imageUrl: _imageUrlController.text.trim().isEmpty
              ? null
              : _imageUrlController.text.trim(),
        );
      }

      // Refresh inventory
      ref.invalidate(shopInventoryProvider(widget.shopId));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(widget.productId == null
                ? 'Product added successfully'
                : 'Product updated successfully'),
          ),
        );
        context.pop();
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
        title: Text(widget.productId == null
            ? 'Add Product'
            : 'Edit Product'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Product name
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Product Name *',
                  border: OutlineInputBorder(),
                ),
                validator: (value) =>
                    value?.isEmpty ?? true ? 'Product name is required' : null,
              ),
              const SizedBox(height: 16),

              // Description
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
              ),
              const SizedBox(height: 16),

              // Category
              TextFormField(
                controller: _categoryController,
                decoration: const InputDecoration(
                  labelText: 'Category *',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., Cement, Steel, Tools',
                ),
                validator: (value) =>
                    value?.isEmpty ?? true ? 'Category is required' : null,
              ),
              const SizedBox(height: 16),

              // Price and Unit
              Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: TextFormField(
                      controller: _priceController,
                      decoration: const InputDecoration(
                        labelText: 'Price *',
                        border: OutlineInputBorder(),
                        prefixText: 'UGX ',
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value?.isEmpty ?? true) {
                          return 'Price is required';
                        }
                        if (double.tryParse(value!) == null) {
                          return 'Invalid price';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: TextFormField(
                      controller: _unitController,
                      decoration: const InputDecoration(
                        labelText: 'Unit *',
                        border: OutlineInputBorder(),
                        hintText: 'kg, piece, bag',
                      ),
                      validator: (value) =>
                          value?.isEmpty ?? true ? 'Unit is required' : null,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Quantity and Min Order
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _quantityController,
                      decoration: const InputDecoration(
                        labelText: 'Quantity Available *',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value?.isEmpty ?? true) {
                          return 'Required';
                        }
                        if (int.tryParse(value!) == null) {
                          return 'Invalid';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: TextFormField(
                      controller: _minOrderController,
                      decoration: const InputDecoration(
                        labelText: 'Min Order *',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value?.isEmpty ?? true) {
                          return 'Required';
                        }
                        final intValue = int.tryParse(value!);
                        if (intValue == null || intValue < 1) {
                          return 'Min: 1';
                        }
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Brand
              TextFormField(
                controller: _brandController,
                decoration: const InputDecoration(
                  labelText: 'Brand',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),

              // Image URL
              TextFormField(
                controller: _imageUrlController,
                decoration: const InputDecoration(
                  labelText: 'Image URL',
                  border: OutlineInputBorder(),
                  hintText: 'https://...',
                ),
                keyboardType: TextInputType.url,
              ),
              const SizedBox(height: 16),

              // Available toggle
              SwitchListTile(
                title: const Text('Product Available'),
                subtitle: const Text('Enable to make product visible to customers'),
                value: _isAvailable,
                onChanged: (value) => setState(() => _isAvailable = value),
              ),
              const SizedBox(height: 32),

              // Save button
              ElevatedButton(
                onPressed: _isLoading ? null : _saveProduct,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Text(widget.productId == null
                        ? 'Add Product'
                        : 'Update Product'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

