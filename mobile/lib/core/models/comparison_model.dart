import 'package:freezed_annotation/freezed_annotation.dart';
import 'product_model.dart';

part 'comparison_model.freezed.dart';
part 'comparison_model.g.dart';

/// Comparison model matching Flask Comparison model
@freezed
class ComparisonModel with _$ComparisonModel {
  const factory ComparisonModel({
    @JsonKey(fromJson: _intFromJson) required int id,
    @JsonKey(name: 'user_id', fromJson: _intFromJson) required int userId,
    @JsonKey(name: 'product_id', fromJson: _intFromJson) required int productId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    // Nested product info (when fetched with details)
    @JsonKey(fromJson: _productFromJson) ProductModel? product,
  }) = _ComparisonModel;

  factory ComparisonModel.fromJson(Map<String, dynamic> json) =>
      _$ComparisonModelFromJson(json);
}

/// Helper function to convert int from JSON
int _intFromJson(dynamic value) {
  if (value == null) return 0;
  if (value is int) return value;
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}

/// Helper function to convert product from JSON
ProductModel? _productFromJson(dynamic value) {
  if (value == null) return null;
  if (value is Map) {
    try {
      return ProductModel.fromJson(Map<String, dynamic>.from(value));
    } catch (e) {
      return null;
    }
  }
  return null;
}
