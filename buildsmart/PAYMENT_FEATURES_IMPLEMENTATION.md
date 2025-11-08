# Payment & Financials Implementation

## Overview
This document details the implementation of Priority 5: Payments & Financials features for BuildSmart.

## Features Implemented

### 1. PDF Invoice Generation
- **Service**: `app/services/invoice_service.py`
- **Routes**: `app/blueprints/api/invoice_routes.py`
- **Library**: ReportLab (4.0.7)
- **Features**:
  - Generate PDF invoices for orders
  - Include order details, items, customer/shop information
  - Display subtotal, discount, tax, and total
  - Payment information and transaction details
  - Professional invoice formatting

**API Endpoints**:
- `GET /api/invoices/<order_id>` - Generate and download invoice PDF
- `GET /api/invoices/<order_id>/download` - Save invoice to file

### 2. Discount/Coupon System
- **Models**: `app/models/coupon.py`
  - `Coupon`: Coupon configuration (code, discount type, value, limits)
  - `CouponUsage`: Track coupon usage history
- **Service**: `app/services/coupon_service.py`
- **Routes**: `app/blueprints/api/coupon_routes.py`
- **Features**:
  - Percentage and fixed amount discounts
  - Usage limits and expiration dates
  - Minimum order amount requirements
  - Maximum discount caps (for percentage coupons)
  - Applicable to all, specific products, categories, or shops
  - Coupon validation and application
  - Usage tracking and statistics

**API Endpoints**:
- `POST /api/coupons/validate` - Validate a coupon code
- `POST /api/coupons/apply` - Apply coupon to order
- `GET /api/coupons` - Get all coupons (admin)
- `POST /api/coupons` - Create new coupon (admin)
- `GET /api/coupons/my-coupons` - Get user's coupon usage history

### 3. Tax Calculation System
- **Models**: `app/models/tax.py`
  - `TaxRate`: Tax rate configuration (VAT, Sales Tax, GST, etc.)
  - `ProductTax`: Product-specific tax assignments
- **Service**: `app/services/tax_service.py`
- **Routes**: `app/blueprints/api/tax_routes.py`
- **Features**:
  - Multiple tax types (VAT, Sales Tax, GST, Custom)
  - Tax rates applicable to all, products, categories, or shops
  - Product-specific tax rates
  - Automatic tax calculation for orders
  - Tax breakdown by type

**API Endpoints**:
- `GET /api/tax/calculate/<order_id>` - Calculate tax for an order
- `GET /api/tax/product/<product_id>` - Get tax rate for a product
- `GET /api/tax/rates` - Get all tax rates
- `POST /api/tax/rates` - Create new tax rate (admin)
- `POST /api/tax/product/<product_id>` - Assign tax rate to product

### 4. Wallet & Transaction Management
- **Models**: `app/models/wallet.py`
  - `Wallet`: User wallet with balance and currency
  - `Transaction`: Transaction history (credit, debit, transfer)
- **Service**: `app/services/wallet_service.py`
- **Routes**: `app/blueprints/api/wallet_routes.py`
- **Features**:
  - Wallet creation and management
  - Credit and debit operations
  - Transaction history with pagination
  - Wallet-to-wallet transfers
  - Transaction references and status tracking
  - Wallet summary with statistics

**API Endpoints**:
- `GET /api/wallet/balance` - Get wallet balance
- `GET /api/wallet/summary` - Get wallet summary
- `GET /api/wallet/transactions` - Get transaction history
- `POST /api/wallet/credit` - Credit wallet
- `POST /api/wallet/debit` - Debit wallet
- `POST /api/wallet/transfer` - Transfer between wallets

## Database Changes

### New Tables
1. **coupons**: Coupon configuration
2. **coupon_usages**: Coupon usage tracking
3. **tax_rates**: Tax rate configuration
4. **product_taxes**: Product-tax assignments
5. **wallets**: User wallets
6. **transactions**: Transaction history

### Order Model Updates
- `subtotal_amount`: Amount before tax and discount
- `discount_amount`: Discount applied (default: 0.00)
- `tax_amount`: Tax amount (default: 0.00)
- `coupon_code`: Applied coupon code

## Migration
- **File**: `migrations/versions/payment_features_migration.py`
- **Revision**: `payment_features_001`
- Run migration: `flask db upgrade`

## Dependencies Added
- `reportlab==4.0.7` - PDF generation
- `pandas==2.1.4` - Data processing (for future reporting features)
- `openpyxl==3.1.2` - Excel file support (for future export features)

## Usage Examples

### Generate Invoice
```python
from app.services.invoice_service import InvoiceService

# Generate PDF buffer
pdf_buffer = InvoiceService.generate_invoice(order_id)

# Save to file
file_path = InvoiceService.save_invoice(order_id)
```

### Apply Coupon
```python
from app.services.coupon_service import CouponService

# Validate coupon
is_valid, error_msg, coupon = CouponService.validate_coupon(
    code='SAVE10',
    user_id=user_id,
    order_amount=1000.00
)

# Apply coupon
success, error_msg, discount_amount = CouponService.apply_coupon(
    order_id=order_id,
    coupon_code='SAVE10'
)
```

### Calculate Tax
```python
from app.services.tax_service import TaxService

# Calculate order tax
total_tax, tax_breakdown = TaxService.calculate_order_tax(order_id)

# Get product tax rate
tax_rate = TaxService.get_product_tax_rate(product_id)
```

### Wallet Operations
```python
from app.services.wallet_service import WalletService

# Credit wallet
transaction = WalletService.credit_wallet(
    user_id=user_id,
    amount=1000.00,
    description='Top-up'
)

# Debit wallet
transaction = WalletService.debit_wallet(
    user_id=user_id,
    amount=500.00,
    description='Payment'
)

# Transfer between wallets
success, error_msg, transactions = WalletService.transfer_between_wallets(
    from_user_id=user_id,
    to_user_id=recipient_id,
    amount=200.00,
    description='Transfer'
)
```

## Security Considerations
- All payment endpoints require authentication (`@login_required`)
- Admin-only endpoints check `current_user.is_admin`
- Order ownership validation for invoice access
- Transaction references are unique and generated securely
- Wallet balance validation before debits

## Future Enhancements
- Payment gateway integration
- Automatic tax calculation during checkout
- Coupon code generation and management UI
- Wallet top-up via payment gateway
- Transaction export to Excel/CSV
- Invoice email delivery
- Tax reporting and analytics
- Multi-currency support

