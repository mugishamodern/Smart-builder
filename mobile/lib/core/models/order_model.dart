import 'package:freezed_annotation/freezed_annotation.dart';
import 'shop_model.dart';
import 'user_model.dart';
import 'product_model.dart';

part 'order_model.freezed.dart';
part 'order_model.g.dart';

/// Order model matching Flask Order model
@freezed
class OrderModel with _$OrderModel {
  const factory OrderModel({
    required int id,
    required String orderNumber,
    @Default('pending') String status, // pending, confirmed, processing, shipped, delivered, cancelled
    required double totalAmount,
    String? deliveryAddress,
    String? deliveryNotes,
    @Default('pending') String paymentStatus, // pending, paid, failed, refunded
    String? paymentMethod,
    required int customerId,
    required int shopId,
    DateTime? createdAt,
    DateTime? updatedAt,
    // Nested data (when fetched with details)
    List<OrderItemModel>? items,
    ShopModel? shop,
    UserModel? customer,
  }) = _OrderModel;

  factory OrderModel.fromJson(Map<String, dynamic> json) =>
      _$OrderModelFromJson(json);
}

/// Order item model matching Flask OrderItem model
@freezed
class OrderItemModel with _$OrderItemModel {
  const factory OrderItemModel({
    required int id,
    required int quantity,
    required double unitPrice,
    required double totalPrice,
    required int orderId,
    required int productId,
    // Nested product info (when fetched with details)
    ProductModel? product,
  }) = _OrderItemModel;

  factory OrderItemModel.fromJson(Map<String, dynamic> json) =>
      _$OrderItemModelFromJson(json);
}

