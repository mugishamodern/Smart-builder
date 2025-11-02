import 'package:freezed_annotation/freezed_annotation.dart';
import 'shop_model.dart';

part 'product_model.freezed.dart';
part 'product_model.g.dart';

/// Product model matching Flask Product model
@freezed
class ProductModel with _$ProductModel {
  const factory ProductModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(fromJson: _stringFromJson) required String name,
    @JsonKey(fromJson: _stringFromJsonNullable) String? description,
    @JsonKey(fromJson: _stringFromJson) required String category,
    @JsonKey(fromJson: _priceFromJson) required double price,
    @JsonKey(fromJson: _stringFromJson) required String unit, // e.g., 'kg', 'piece', 'bag', 'm2'
    @JsonKey(name: 'quantity_available', fromJson: _quantityFromJson, defaultValue: 0) @Default(0) int quantityAvailable,
    @JsonKey(name: 'min_order_quantity', defaultValue: 1) @Default(1) int minOrderQuantity,
    @JsonKey(name: 'is_available', defaultValue: true) @Default(true) bool isAvailable,
    @JsonKey(name: 'image_url', fromJson: _stringFromJsonNullable) String? imageUrl,
    @JsonKey(fromJson: _stringFromJsonNullable) String? brand,
    @JsonKey(fromJson: _specificationsFromJson) Map<String, dynamic>? specifications, // Additional specs as JSON
    @JsonKey(name: 'shop_id', fromJson: _intFromJson) required int shopId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    // Nested shop info (when fetched with shop details)
    @JsonKey(fromJson: _shopFromJson) ShopModel? shop,
  }) = _ProductModel;

  factory ProductModel.fromJson(Map<String, dynamic> json) =>
      _$ProductModelFromJson(json);
}

/// Helper function to convert int from JSON (handles null, string, and number)
int _intFromJson(dynamic value) {
  if (value == null) {
    return 0;
  }
  if (value is num) {
    return value.toInt();
  } else if (value is String) {
    try {
      return int.parse(value);
    } catch (e) {
      return 0;
    }
  } else {
    return 0;
  }
}

/// Helper function to convert string from JSON (handles null)
String _stringFromJson(dynamic value) {
  if (value == null) return '';
  if (value is String) return value;
  return value.toString();
}

/// Helper function to convert nullable string from JSON
String? _stringFromJsonNullable(dynamic value) {
  if (value == null) return null;
  if (value is String) return value.isEmpty ? null : value;
  return value.toString();
}

/// Helper function to convert price from JSON (handles both string and number)
double _priceFromJson(dynamic value) {
  if (value == null) throw ArgumentError('Price cannot be null');
  if (value is num) {
    return value.toDouble();
  } else if (value is String) {
    return double.parse(value);
  } else {
    throw ArgumentError('Price must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert quantity from JSON (handles both string and number)
int _quantityFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is num) {
    return value.toInt();
  } else if (value is String) {
    return int.parse(value);
  } else {
    throw ArgumentError('Quantity must be a number or string, got ${value.runtimeType}');
  }
}

/// Helper function to convert specifications from JSON (handles LinkedMap)
Map<String, dynamic>? _specificationsFromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    return Map<String, dynamic>.from(value);
  } else {
    throw ArgumentError('Specifications must be a Map, got ${value.runtimeType}');
  }
}

/// Helper function to convert shop from JSON (handles LinkedMap)
ShopModel? _shopFromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    return ShopModel.fromJson(Map<String, dynamic>.from(value));
  } else {
    throw ArgumentError('Shop must be a Map, got ${value.runtimeType}');
  }
}

extension ProductModelExtension on ProductModel {
  bool get isInStock => quantityAvailable > 0 && isAvailable;
}

