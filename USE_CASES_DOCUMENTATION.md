# BuildSmart - Comprehensive Use Cases Documentation

This document provides a complete overview of all use cases for the BuildSmart application, covering both the Flask backend (website) and Flutter mobile app.

## Table of Contents

1. [User Roles](#user-roles)
2. [Website Use Cases](#website-use-cases)
3. [Mobile App Use Cases](#mobile-app-use-cases)
4. [API Endpoints](#api-endpoints)
5. [System Features](#system-features)

---

## User Roles

### 1. Guest User (Unauthenticated)
- Can browse products, shops, and services
- Can search for products, shops, and services
- Can view shop details and product information
- Can view shop locations on map
- Can add products to cart (stored in session)
- Can view nearby shops
- Cannot place orders (must register/login)
- Cannot access messaging features
- Cannot save recommendations
- Cannot compare products

### 2. Customer (Authenticated)
- All guest user capabilities
- Can register and login
- Can place orders
- Can manage shopping cart
- Can save multiple delivery addresses
- Can view order history
- Can submit reviews and ratings
- Can use AI recommendations
- Can save and manage recommendations
- Can compare products
- Can save carts for later
- Can message shop owners and other users
- Can receive real-time messages via WebSocket
- Can view unread message count

### 3. Shop Owner (Authenticated)
- All customer capabilities
- Can register a shop
- Can manage shop inventory (add, edit, delete products)
- Can view shop dashboard with analytics
- Can view shop orders
- Can update order status
- Can view sales trends and statistics
- Can view top products chart
- Can manage shop profile
- Can receive messages from customers
- Can view shop verification status

### 4. Service Provider (Authenticated)
- All customer capabilities
- Can register services
- Can manage service listings
- Can receive service inquiries

### 5. Admin (Authenticated)
- All shop owner capabilities
- Can access admin dashboard
- Can verify/reject shops
- Can manage all users
- Can view all shops and orders
- Can manage payments (release, refund)
- Can view analytics and reports
- Can view all conversations
- Can manage system settings

---

## Website Use Cases

### Authentication & Registration

#### UC-WEB-001: User Registration
**Actor**: Guest User  
**Description**: New user registers for an account  
**Preconditions**: User is not logged in  
**Steps**:
1. User navigates to registration page
2. User selects user type (customer, shop_owner, service_provider)
3. User fills in registration form (username, email, password, full_name, phone)
4. User submits form
5. System validates input
6. System creates user account
7. User is redirected to login page

**Postconditions**: User account created, user can now login

#### UC-WEB-002: User Login
**Actor**: Registered User  
**Description**: User logs into their account  
**Preconditions**: User has registered account  
**Steps**:
1. User navigates to login page
2. User enters username and password
3. User submits form
4. System validates credentials
5. System creates session
6. System merges guest cart with user cart (if applicable)
7. User is redirected to dashboard

**Postconditions**: User is logged in, session created, cart merged

#### UC-WEB-003: User Logout
**Actor**: Authenticated User  
**Description**: User logs out of their account  
**Steps**:
1. User clicks logout button
2. System destroys session
3. User is redirected to home page

**Postconditions**: User is logged out, session destroyed

---

### Product & Shop Browsing

#### UC-WEB-004: Browse Home Page
**Actor**: Any User  
**Description**: User views featured content on home page  
**Steps**:
1. User navigates to home page
2. System displays featured shops (verified, active)
3. System displays featured products (available)
4. System displays featured services (available)

**Output**: Home page with featured content

#### UC-WEB-005: Search Products, Shops, Services
**Actor**: Any User  
**Description**: User searches for products, shops, or services  
**Steps**:
1. User navigates to search page
2. User enters search query
3. Optionally selects category filter
4. User submits search
5. System searches across products, shops, and services
6. System displays results grouped by type

**Output**: Search results page with products, shops, and services

#### UC-WEB-006: View Product Details
**Actor**: Any User  
**Description**: User views detailed information about a product  
**Steps**:
1. User clicks on a product
2. System displays product details (name, description, price, quantity, unit, category)
3. System displays shop information
4. System displays product reviews (if any)
5. User can add product to cart (if authenticated)

**Output**: Product detail page

#### UC-WEB-007: View Shop Details
**Actor**: Any User  
**Description**: User views detailed information about a shop  
**Steps**:
1. User clicks on a shop
2. System displays shop information (name, address, rating, verification status)
3. System displays shop products
4. System displays shop reviews
5. System displays shop location on map (if coordinates available)
6. User can view shop on map
7. User can message shop owner (if authenticated)

**Output**: Shop detail page

#### UC-WEB-008: View Nearby Shops on Map
**Actor**: Any User  
**Description**: User views shops on interactive map with location-based filtering  
**Steps**:
1. User navigates to map page
2. System requests user location (if permission granted)
3. System displays map with shop markers
4. User can filter by category
5. User can click markers to see shop info
6. System calculates and displays distances

**Output**: Interactive map with shop locations

#### UC-WEB-009: Advanced Product Search with Filters
**Actor**: Any User  
**Description**: User searches products with advanced filters  
**Steps**:
1. User navigates to search page
2. User enters search query
3. User applies filters:
   - Category
   - Price range (min/max)
   - Shop rating
   - Shop verification status
   - Distance from location
4. User selects sort option (relevance, price, rating, distance)
5. System filters and sorts products
6. System displays paginated results

**Output**: Filtered and sorted product results

---

### Shopping Cart & Checkout

#### UC-WEB-010: Add Product to Cart
**Actor**: Any User  
**Description**: User adds a product to shopping cart  
**Preconditions**: Product is available  
**Steps**:
1. User views product detail page
2. User selects quantity
3. User clicks "Add to Cart"
4. System creates/updates cart (guest session or user account)
5. System updates cart item quantity if product already in cart
6. System displays success message

**Postconditions**: Product added to cart, cart count updated

#### UC-WEB-011: View Shopping Cart
**Actor**: Any User  
**Description**: User views their shopping cart  
**Steps**:
1. User clicks cart icon in navbar
2. System retrieves cart (session-based or user-based)
3. System displays cart items with quantities and prices
4. System displays cart total
5. User can update quantities
6. User can remove items
7. User can clear cart
8. User can proceed to checkout (if authenticated)

**Output**: Shopping cart page

#### UC-WEB-012: Update Cart Item Quantity
**Actor**: Any User  
**Description**: User updates quantity of a cart item  
**Steps**:
1. User views shopping cart
2. User changes quantity for an item
3. System validates quantity (available stock)
4. System updates cart item
5. System recalculates cart total
6. System displays updated cart

**Postconditions**: Cart item quantity updated, total recalculated

#### UC-WEB-013: Remove Item from Cart
**Actor**: Any User  
**Description**: User removes an item from cart  
**Steps**:
1. User views shopping cart
2. User clicks remove button for an item
3. System removes item from cart
4. System recalculates cart total
5. System displays updated cart

**Postconditions**: Item removed from cart

#### UC-WEB-014: Save Cart for Later
**Actor**: Authenticated Customer  
**Description**: User saves their current cart for later use  
**Steps**:
1. User views shopping cart
2. User clicks "Save Cart" button
3. System marks cart as saved
4. System displays success message

**Postconditions**: Cart saved, accessible from saved carts page

#### UC-WEB-015: View Saved Carts
**Actor**: Authenticated Customer  
**Description**: User views their saved carts  
**Steps**:
1. User navigates to saved carts page
2. System retrieves user's saved carts
3. System displays list of saved carts with items
4. User can restore a saved cart
5. User can delete a saved cart

**Output**: Saved carts page

#### UC-WEB-016: Restore Saved Cart
**Actor**: Authenticated Customer  
**Description**: User restores a saved cart to active cart  
**Steps**:
1. User views saved carts
2. User clicks "Restore" on a saved cart
3. System merges saved cart items with current cart
4. System marks saved cart as active
5. User is redirected to cart page

**Postconditions**: Saved cart restored, items merged with current cart

#### UC-WEB-017: Checkout Process
**Actor**: Authenticated Customer  
**Description**: User completes checkout and places order  
**Preconditions**: User has items in cart, user is logged in  
**Steps**:
1. User views shopping cart
2. User clicks "Checkout"
3. System displays checkout page
4. User selects delivery address (from saved addresses or enters new)
5. User enters delivery notes (optional)
6. User selects payment method (cash_on_delivery, mobile_money, bank_transfer)
7. User reviews order summary
8. User clicks "Place Order"
9. System validates cart and addresses
10. System creates order(s) - one per shop
11. System creates payment record(s)
12. System clears cart
13. System displays order confirmation

**Postconditions**: Order created, payment record created, cart cleared

---

### Address Management

#### UC-WEB-018: View Address Book
**Actor**: Authenticated Customer  
**Description**: User views their saved delivery addresses  
**Steps**:
1. User navigates to Address Book page
2. System retrieves user's addresses
3. System displays list of addresses with labels
4. User can add new address
5. User can edit existing address
6. User can delete address
7. User can set default address

**Output**: Address book page

#### UC-WEB-019: Add New Address
**Actor**: Authenticated Customer  
**Description**: User adds a new delivery address  
**Steps**:
1. User navigates to Address Book
2. User clicks "Add New Address"
3. User fills in address form (label, full_name, phone, address_line1, address_line2, city, state, postal_code, country)
4. User optionally sets as default
5. User submits form
6. System validates input
7. System creates address record
8. System updates default addresses if needed
9. System displays success message

**Postconditions**: New address saved

#### UC-WEB-020: Edit Address
**Actor**: Authenticated Customer  
**Description**: User edits an existing address  
**Steps**:
1. User views Address Book
2. User clicks "Edit" on an address
3. System displays address form pre-filled with current data
4. User modifies fields
5. User submits form
6. System validates input
7. System updates address record
8. System displays success message

**Postconditions**: Address updated

#### UC-WEB-021: Delete Address
**Actor**: Authenticated Customer  
**Description**: User deletes an address  
**Steps**:
1. User views Address Book
2. User clicks "Delete" on an address
3. System confirms deletion
4. System deletes address record
5. System displays success message

**Postconditions**: Address deleted

#### UC-WEB-022: Set Default Address
**Actor**: Authenticated Customer  
**Description**: User sets an address as default  
**Steps**:
1. User views Address Book
2. User clicks "Set as Default" on an address
3. System updates default flag (removes from previous default)
4. System saves changes
5. System displays success message

**Postconditions**: Default address updated

---

### Orders

#### UC-WEB-023: View Order History
**Actor**: Authenticated Customer  
**Description**: User views their past orders  
**Steps**:
1. User navigates to "My Orders" page
2. System retrieves user's orders
3. System displays orders with details (order number, date, status, total)
4. User can filter by status
5. User can view order details
6. User can cancel pending orders

**Output**: Orders list page

#### UC-WEB-024: View Order Details
**Actor**: Authenticated Customer  
**Description**: User views detailed information about an order  
**Steps**:
1. User views order history
2. User clicks on an order
3. System displays order details:
   - Order number and date
   - Shop information
   - Order items with quantities and prices
   - Delivery address
   - Payment information
   - Order status
   - Payment status
4. User can cancel order (if pending)
5. User can submit review (if order completed)

**Output**: Order detail page

#### UC-WEB-025: Cancel Order
**Actor**: Authenticated Customer  
**Description**: User cancels a pending order  
**Preconditions**: Order status is "pending"  
**Steps**:
1. User views order details
2. User clicks "Cancel Order"
3. System confirms cancellation
4. System updates order status to "cancelled"
5. System restores product quantities
6. System updates payment status
7. System displays success message

**Postconditions**: Order cancelled, stock restored

---

### Reviews & Ratings

#### UC-WEB-026: Submit Review
**Actor**: Authenticated Customer  
**Description**: User submits a review for a shop or product  
**Steps**:
1. User views order details or shop page
2. User clicks "Write Review" or "Submit Review"
3. User selects rating (1-5 stars)
4. User enters review comment
5. User submits review
6. System validates input
7. System creates/updates review record
8. System updates shop rating average
9. System displays success message

**Postconditions**: Review submitted, shop rating updated

#### UC-WEB-027: View Shop Reviews
**Actor**: Any User  
**Description**: User views reviews for a shop  
**Steps**:
1. User views shop detail page
2. System displays shop reviews:
   - Reviewer name
   - Rating
   - Comment
   - Date
   - Verified purchase badge (if applicable)
3. User can read all reviews
4. Reviews are sorted by date (newest first)

**Output**: Reviews section on shop page

---

### AI Recommendations

#### UC-WEB-028: Generate AI Recommendation
**Actor**: Authenticated Customer  
**Description**: User generates AI-powered material recommendations for a project  
**Steps**:
1. User navigates to Recommendations page
2. User clicks "Get Recommendation"
3. User enters project description
4. User selects project type (2_bedroom_house, 3_bedroom_house, office_building, commercial_building)
5. User optionally provides custom specifications
6. User submits request
7. System generates recommendation:
   - Material recommendations with quantities
   - Cost estimates
   - Service recommendations
   - Shopping plan with nearby shops
8. System displays recommendation
9. User can save recommendation
10. User can view recommendation details

**Output**: AI-generated recommendation with materials, costs, and shopping plan

#### UC-WEB-029: View Saved Recommendations
**Actor**: Authenticated Customer  
**Description**: User views their saved recommendations  
**Steps**:
1. User navigates to Recommendations page
2. System retrieves user's saved recommendations
3. System displays recommendations with project type and cost
4. User can view recommendation details
5. User can delete recommendation

**Output**: Recommendations list page

#### UC-WEB-030: View Recommendation Details
**Actor**: Authenticated Customer  
**Description**: User views detailed recommendation information  
**Steps**:
1. User views saved recommendations
2. User clicks on a recommendation
3. System displays:
   - Project description
   - Recommended materials with quantities
   - Cost breakdown
   - Service recommendations
   - Shopping plan with shop locations
4. User can add recommended materials to cart

**Output**: Recommendation detail page

---

### Product Comparison

#### UC-WEB-031: Add Product to Comparison
**Actor**: Authenticated Customer  
**Description**: User adds a product to comparison list  
**Steps**:
1. User views product detail page
2. User clicks "Compare" button
3. System adds product to comparison list
4. System displays success message

**Postconditions**: Product added to comparison

#### UC-WEB-032: View Product Comparison
**Actor**: Authenticated Customer  
**Description**: User views compared products side-by-side  
**Steps**:
1. User navigates to Comparisons page
2. System retrieves user's comparison list
3. System displays products in comparison table:
   - Product name and image
   - Price
   - Shop name and location
   - Rating
   - Availability
4. User can remove products from comparison
5. User can clear all comparisons
6. User can add products to cart

**Output**: Product comparison page

#### UC-WEB-033: Remove Product from Comparison
**Actor**: Authenticated Customer  
**Description**: User removes a product from comparison  
**Steps**:
1. User views comparison page
2. User clicks "Remove" on a product
3. System removes product from comparison
4. System displays updated comparison

**Postconditions**: Product removed from comparison

#### UC-WEB-034: Clear All Comparisons
**Actor**: Authenticated Customer  
**Description**: User clears all products from comparison  
**Steps**:
1. User views comparison page
2. User clicks "Clear All"
3. System confirms action
4. System removes all products from comparison
5. System displays success message

**Postconditions**: All comparisons cleared

---

### Messaging

#### UC-WEB-035: View Inbox
**Actor**: Authenticated User  
**Description**: User views their message conversations  
**Steps**:
1. User navigates to Messages/Inbox page
2. System retrieves user's conversations
3. System displays conversations:
   - Other participant name
   - Last message preview
   - Timestamp
   - Unread count badge
4. System displays unread count in navbar
5. User can click conversation to open chat
6. System updates in real-time via WebSocket

**Output**: Inbox page with conversations list

#### UC-WEB-036: Send Message
**Actor**: Authenticated User  
**Description**: User sends a message to another user  
**Steps**:
1. User views chat page or shop detail page
2. User clicks "Message" button (if on shop page)
3. User enters message content
4. User sends message
5. System creates message record
6. System creates/updates conversation
7. System emits WebSocket event to receiver
8. System displays message in chat
9. Receiver gets real-time notification (if online)

**Postconditions**: Message sent, conversation updated, real-time notification sent

#### UC-WEB-037: View Chat Conversation
**Actor**: Authenticated User  
**Description**: User views chat conversation with another user  
**Steps**:
1. User clicks on conversation from inbox
2. System retrieves conversation messages
3. System displays messages in chronological order
4. System marks messages as read
5. User can type and send new messages
6. System updates chat in real-time via WebSocket
7. System displays browser notification for new messages (if enabled)

**Output**: Chat page with message history

#### UC-WEB-038: Mark Messages as Read
**Actor**: Authenticated User  
**Description**: System marks messages as read when user views conversation  
**Steps**:
1. User opens chat conversation
2. System automatically marks unread messages as read
3. System updates unread count
4. System emits WebSocket event to sender (optional)

**Postconditions**: Messages marked as read, unread count updated

#### UC-WEB-039: Receive Real-time Message Notifications
**Actor**: Authenticated User  
**Description**: User receives real-time notifications for new messages  
**Steps**:
1. User is logged in and has WebSocket connection
2. Another user sends message
3. System emits WebSocket event to receiver
4. System displays browser notification (if permission granted)
5. System updates unread count in navbar
6. System updates inbox if open

**Postconditions**: Real-time notification displayed, unread count updated

---

### Shop Owner Features

#### UC-WEB-040: Register Shop
**Actor**: Authenticated User (Shop Owner)  
**Description**: User registers a new shop  
**Steps**:
1. User navigates to Shop Registration page
2. User fills in shop details:
   - Shop name
   - Address
   - Description
   - Phone
   - Email
   - Category
   - Location coordinates (optional)
3. User submits form
4. System validates input
5. System creates shop record (is_verified=False by default)
6. System displays success message
7. Shop appears in dashboard with "Pending" status

**Postconditions**: Shop registered, pending admin verification

#### UC-WEB-041: View Shop Dashboard
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner views their shop management dashboard  
**Steps**:
1. User navigates to Shop Dashboard
2. System retrieves user's shops
3. System displays shop cards with:
   - Shop name and status
   - Product count
   - Rating and review count
   - Total orders
   - Total sales
4. System displays sales trends chart (last 30 days)
5. System displays top products chart
6. User can manage inventory
7. User can view orders

**Output**: Shop dashboard with analytics

#### UC-WEB-042: Manage Shop Inventory
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner manages products in their shop  
**Steps**:
1. User navigates to Shop Dashboard
2. User clicks "Manage Inventory" on a shop
3. System displays product list for shop
4. User can:
   - Add new product
   - Edit existing product
   - Delete product
   - Update product availability
   - Update product quantity

**Output**: Inventory management page

#### UC-WEB-043: Add Product to Shop
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner adds a new product to their shop  
**Steps**:
1. User views inventory management
2. User clicks "Add Product"
3. User fills in product form:
   - Product name
   - Description
   - Category
   - Price
   - Quantity available
   - Unit (bags, kg, pieces, etc.)
   - Image (optional)
4. User submits form
5. System validates input
6. System creates product record
7. System displays success message

**Postconditions**: Product added to shop inventory

#### UC-WEB-044: Edit Product
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner edits an existing product  
**Steps**:
1. User views inventory management
2. User clicks "Edit" on a product
3. System displays product form pre-filled with current data
4. User modifies fields
5. User submits form
6. System validates input
7. System updates product record
8. System displays success message

**Postconditions**: Product updated

#### UC-WEB-045: View Shop Orders
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner views orders for their shop  
**Steps**:
1. User navigates to Shop Dashboard
2. User clicks "View Orders" on a shop
3. System retrieves shop orders
4. System displays orders with:
   - Order number
   - Customer information
   - Order items
   - Order total
   - Delivery address
   - Order status
   - Payment status
5. User can update order status
6. User can view order details

**Output**: Shop orders page

#### UC-WEB-046: Update Order Status
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner updates the status of an order  
**Steps**:
1. User views shop orders
2. User selects order
3. User changes order status (pending, processing, shipped, delivered, cancelled)
4. System validates status transition
5. System updates order record
6. System notifies customer (if applicable)
7. System displays success message

**Postconditions**: Order status updated

---

### Admin Features

#### UC-WEB-047: View Admin Dashboard
**Actor**: Admin User  
**Description**: Admin views system overview dashboard  
**Steps**:
1. Admin navigates to Admin Dashboard
2. System displays statistics:
   - Total shops
   - Total customers
   - Total sales
   - Pending shop verifications
   - Pending payments
3. System displays recent orders
4. System displays recent shop registrations
5. System displays pending verifications
6. Admin can access management pages

**Output**: Admin dashboard with system statistics

#### UC-WEB-048: Manage Shops (Admin)
**Actor**: Admin User  
**Description**: Admin views and manages all shops  
**Steps**:
1. Admin navigates to Shops Management page
2. System retrieves all shops
3. System displays shops with filters:
   - Verification status
   - Active status
4. Admin can view shop details
5. Admin can verify/reject shops
6. Admin can activate/deactivate shops

**Output**: Shops management page

#### UC-WEB-049: Verify Shop
**Actor**: Admin User  
**Description**: Admin verifies a shop registration  
**Steps**:
1. Admin views shop details
2. Admin reviews shop information
3. Admin clicks "Verify Shop"
4. System updates shop.is_verified = True
5. System displays success message
6. Shop owner is notified (if applicable)

**Postconditions**: Shop verified, appears in verified shop listings

#### UC-WEB-050: Reject Shop
**Actor**: Admin User  
**Description**: Admin rejects a shop registration  
**Steps**:
1. Admin views shop details
2. Admin reviews shop information
3. Admin clicks "Reject Shop"
4. System updates shop.is_active = False or deletes shop
5. System displays success message
6. Shop owner is notified (if applicable)

**Postconditions**: Shop rejected/inactivated

#### UC-WEB-051: Manage Payments (Admin)
**Actor**: Admin User  
**Description**: Admin manages payment transactions  
**Steps**:
1. Admin navigates to Payments Management page
2. System retrieves all payments
3. System displays payments with filters:
   - Payment status
   - Payment method
4. Admin can view payment details
5. Admin can release held payments
6. Admin can process refunds

**Output**: Payments management page

#### UC-WEB-052: Release Payment
**Actor**: Admin User  
**Description**: Admin releases a payment held in escrow  
**Steps**:
1. Admin views payment details
2. Admin verifies order completion
3. Admin clicks "Release Payment"
4. System updates payment status
5. System transfers funds to shop owner
6. System displays success message

**Postconditions**: Payment released to shop owner

#### UC-WEB-053: Refund Payment
**Actor**: Admin User  
**Description**: Admin processes a payment refund  
**Steps**:
1. Admin views payment details
2. Admin verifies refund reason
3. Admin clicks "Refund Payment"
4. System updates payment status to "refunded"
5. System processes refund to customer
6. System updates order status
7. System displays success message

**Postconditions**: Payment refunded, order updated

#### UC-WEB-054: View Analytics
**Actor**: Admin User  
**Description**: Admin views system analytics and reports  
**Steps**:
1. Admin navigates to Analytics page
2. System displays:
   - Sales trends (last 30 days)
   - Popular products
   - Top shops by revenue
   - Category distribution
   - Sales by day chart
3. Admin can export reports (if implemented)

**Output**: Analytics dashboard with charts and statistics

#### UC-WEB-055: Manage Users (Admin)
**Actor**: Admin User  
**Description**: Admin views and manages all users  
**Steps**:
1. Admin navigates to Users Management page
2. System retrieves all users
3. System displays users with filters:
   - User type
   - Active status
4. Admin can view user details
5. Admin can activate/deactivate users
6. Admin can view user orders and activity

**Output**: Users management page

---

## Mobile App Use Cases

### Authentication

#### UC-MOB-001: User Login (Mobile)
**Actor**: Registered User  
**Description**: User logs into mobile app  
**Steps**:
1. User opens app
2. User enters username and password
3. User taps "Login"
4. App sends login request to API
5. App receives authentication token
6. App stores token securely
7. App connects to WebSocket for messaging
8. App syncs guest cart (if any)
9. App navigates to home/dashboard

**Postconditions**: User logged in, token stored, WebSocket connected

#### UC-MOB-002: User Registration (Mobile)
**Actor**: New User  
**Description**: User registers new account via mobile app  
**Steps**:
1. User opens app
2. User taps "Register"
3. User selects user type
4. User fills registration form
5. User submits form
6. App sends registration request to API
7. App receives confirmation
8. App navigates to login screen

**Postconditions**: Account created

#### UC-MOB-003: User Logout (Mobile)
**Actor**: Authenticated User  
**Description**: User logs out of mobile app  
**Steps**:
1. User opens app settings/profile
2. User taps "Logout"
3. App clears stored authentication token
4. App disconnects WebSocket
5. App clears user data
6. App navigates to login screen

**Postconditions**: User logged out, session cleared

---

### Product & Shop Browsing (Mobile)

#### UC-MOB-004: Browse Home (Mobile)
**Actor**: Any User  
**Description**: User views home screen with featured content  
**Steps**:
1. User opens app
2. App displays featured shops
3. App displays featured products
4. App displays featured services
5. User can scroll through content
6. User can tap items to view details

**Output**: Home screen with featured content

#### UC-MOB-005: Search Products (Mobile)
**Actor**: Any User  
**Description**: User searches for products with filters  
**Steps**:
1. User navigates to search screen
2. User enters search query
3. User applies filters (category, price, rating, distance)
4. User taps "Search"
5. App sends search request to API
6. App displays results
7. User can sort results
8. User can tap product to view details

**Output**: Search results screen

#### UC-MOB-006: View Product Details (Mobile)
**Actor**: Any User  
**Description**: User views product details on mobile  
**Steps**:
1. User taps on a product
2. App displays product details:
   - Product name and image
   - Description
   - Price and availability
   - Shop information
   - Reviews
3. User can add to cart (if authenticated)
4. User can add to comparison (if authenticated)
5. User can view shop details

**Output**: Product detail screen

#### UC-MOB-007: View Nearby Shops Map (Mobile)
**Actor**: Any User  
**Description**: User views shops on map with location  
**Steps**:
1. User navigates to map screen
2. App requests location permission
3. App gets user location
4. App sends nearby shops request to API
5. App displays map with shop markers
6. User can tap markers to see shop info
7. User can filter by category
8. App displays distances

**Output**: Map screen with shop locations

---

### Shopping Cart (Mobile)

#### UC-MOB-008: Add to Cart (Mobile)
**Actor**: Any User  
**Description**: User adds product to cart via mobile app  
**Steps**:
1. User views product details
2. User selects quantity
3. User taps "Add to Cart"
4. App sends request to API (or stores locally for guest)
5. App updates cart count badge
6. App displays success message
7. Cart syncs with server on login (if guest)

**Postconditions**: Product added to cart

#### UC-MOB-009: View Cart (Mobile)
**Actor**: Any User  
**Description**: User views shopping cart on mobile  
**Steps**:
1. User taps cart icon
2. App retrieves cart (from API or local storage)
3. App displays cart items
4. User can update quantities
5. User can remove items
6. User can proceed to checkout (if authenticated)

**Output**: Cart screen

#### UC-MOB-010: Update Cart Item (Mobile)
**Actor**: Any User  
**Description**: User updates cart item quantity on mobile  
**Steps**:
1. User views cart
2. User changes quantity using +/- buttons
3. App sends update request to API
4. App updates cart total
5. App displays updated cart

**Postconditions**: Cart item updated

#### UC-MOB-011: Checkout (Mobile)
**Actor**: Authenticated Customer  
**Description**: User completes checkout on mobile  
**Steps**:
1. User views cart
2. User taps "Checkout"
3. App displays checkout form
4. User selects delivery address (from saved addresses)
5. User enters delivery notes
6. User selects payment method
7. User reviews order summary
8. User taps "Place Order"
9. App sends order request to API
10. App receives order confirmation
11. App clears cart
12. App navigates to order confirmation screen

**Postconditions**: Order placed, cart cleared

---

### Orders (Mobile)

#### UC-MOB-012: View Orders (Mobile)
**Actor**: Authenticated Customer  
**Description**: User views order history on mobile  
**Steps**:
1. User navigates to Orders screen
2. App sends request to API
3. App displays orders list
4. User can filter by status
5. User can tap order to view details
6. User can cancel pending orders

**Output**: Orders list screen

#### UC-MOB-013: View Order Details (Mobile)
**Actor**: Authenticated Customer  
**Description**: User views order details on mobile  
**Steps**:
1. User taps on an order
2. App displays order details:
   - Order number and date
   - Shop information
   - Order items
   - Delivery address
   - Payment information
   - Status
3. User can track order (if implemented)
4. User can submit review

**Output**: Order detail screen

---

### Messaging (Mobile)

#### UC-MOB-014: View Inbox (Mobile)
**Actor**: Authenticated User  
**Description**: User views message conversations on mobile  
**Steps**:
1. User navigates to Messages/Inbox screen
2. App connects to WebSocket (if not connected)
3. App sends request to API for conversations
4. App displays conversations list
5. App displays unread count badge
6. User can tap conversation to open chat
7. App receives real-time updates via WebSocket

**Output**: Inbox screen with conversations

#### UC-MOB-015: Send Message (Mobile)
**Actor**: Authenticated User  
**Description**: User sends message via mobile app  
**Steps**:
1. User opens chat conversation
2. User types message
3. User taps send button
4. App sends message via WebSocket
5. App also sends via API (for persistence)
6. App displays message in chat
7. Receiver gets push notification (if implemented)

**Postconditions**: Message sent, real-time delivery

#### UC-MOB-016: Receive Real-time Messages (Mobile)
**Actor**: Authenticated User  
**Description**: User receives real-time messages via WebSocket  
**Steps**:
1. User has app open and WebSocket connected
2. Another user sends message
3. App receives WebSocket event
4. App displays message in chat (if chat open)
5. App updates inbox (if inbox visible)
6. App shows push notification (if app in background)
7. App updates unread count badge

**Postconditions**: Real-time message received, notification shown

---

### Product Comparison (Mobile)

#### UC-MOB-017: Add to Comparison (Mobile)
**Actor**: Authenticated Customer  
**Description**: User adds product to comparison on mobile  
**Steps**:
1. User views product details
2. User taps "Compare" button
3. App sends request to API (or stores locally for guest)
4. App displays success message
5. Product added to comparison list

**Postconditions**: Product added to comparison

#### UC-MOB-018: View Comparison (Mobile)
**Actor**: Authenticated Customer  
**Description**: User views compared products on mobile  
**Steps**:
1. User navigates to Comparisons screen
2. App retrieves comparison list
3. App displays products in comparison view
4. User can scroll horizontally to compare
5. User can remove products
6. User can clear all
7. User can add products to cart

**Output**: Comparison screen

---

### AI Recommendations (Mobile)

#### UC-MOB-019: Generate Recommendation (Mobile)
**Actor**: Authenticated Customer  
**Description**: User generates AI recommendation on mobile  
**Steps**:
1. User navigates to Recommendations screen
2. User taps "Get Recommendation"
3. User enters project description
4. User selects project type
5. User provides custom specs (optional)
6. User taps "Generate"
7. App sends request to API
8. App displays recommendation:
   - Materials list
   - Cost breakdown
   - Service recommendations
   - Shopping plan
9. User can save recommendation

**Output**: Recommendation detail screen

#### UC-MOB-020: View Saved Recommendations (Mobile)
**Actor**: Authenticated Customer  
**Description**: User views saved recommendations on mobile  
**Steps**:
1. User navigates to Recommendations screen
2. App retrieves saved recommendations
3. App displays recommendations list
4. User can tap to view details
5. User can delete recommendations

**Output**: Recommendations list screen

---

### Shop Owner Features (Mobile)

#### UC-MOB-021: View Shop Dashboard (Mobile)
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner views dashboard on mobile  
**Steps**:
1. User navigates to Shop Dashboard
2. App retrieves user's shops
3. App displays shop cards with statistics
4. User can view sales charts
5. User can manage inventory
6. User can view orders

**Output**: Shop dashboard screen

#### UC-MOB-022: Manage Inventory (Mobile)
**Actor**: Authenticated Shop Owner  
**Description**: Shop owner manages products on mobile  
**Steps**:
1. User views shop dashboard
2. User taps "Manage Inventory"
3. App displays product list
4. User can add products
5. User can edit products
6. User can update quantities
7. User can toggle availability

**Output**: Inventory management screen

---

### User Profile & Settings (Mobile)

#### UC-MOB-023: View Profile (Mobile)
**Actor**: Authenticated User  
**Description**: User views and edits profile on mobile  
**Steps**:
1. User navigates to Profile screen
2. App displays user information
3. User can edit profile details
4. User can change password
5. User can update location
6. User can view account settings

**Output**: Profile screen

#### UC-MOB-024: Manage Addresses (Mobile)
**Actor**: Authenticated Customer  
**Description**: User manages delivery addresses on mobile  
**Steps**:
1. User navigates to Address Book
2. App retrieves saved addresses
3. App displays addresses list
4. User can add new address
5. User can edit address
6. User can delete address
7. User can set default address

**Output**: Address book screen

---

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Product Endpoints
- `GET /api/products/search` - Search products with filters
- `GET /shop/<id>/product/<id>` - Get product details
- `GET /api/categories` - Get product categories

### Shop Endpoints
- `GET /api/shops/nearby` - Get nearby shops
- `GET /api/shops/search` - Search shops
- `GET /shop/<id>` - Get shop details
- `GET /api/shop/<id>/products` - Get shop products
- `GET /api/shop/<id>/reviews` - Get shop reviews

### Cart Endpoints
- `GET /api/user/cart` - Get user cart
- `POST /api/user/cart/add` - Add product to cart
- `PUT /api/user/cart/item/<id>/update` - Update cart item
- `DELETE /api/user/cart/item/<id>/remove` - Remove cart item
- `DELETE /api/user/cart/clear` - Clear cart
- `POST /api/user/cart/save` - Save cart
- `GET /api/user/cart/saved` - Get saved carts
- `POST /api/user/cart/restore/<id>` - Restore saved cart
- `DELETE /api/user/cart/<id>/delete` - Delete saved cart

### Checkout Endpoints
- `POST /api/user/checkout/place-order` - Place order

### Order Endpoints
- `GET /api/user/orders` - Get user orders
- `GET /api/user/orders/<id>` - Get order details
- `POST /api/orders/<id>/cancel` - Cancel order

### Address Endpoints
- `GET /api/user/addresses` - Get user addresses
- `POST /api/user/addresses` - Create address
- `PUT /api/user/addresses/<id>` - Update address
- `DELETE /api/user/addresses/<id>` - Delete address
- `PUT /api/user/addresses/<id>/set-default` - Set default address

### Review Endpoints
- `POST /api/reviews/submit` - Submit review
- `GET /api/shop/<id>/reviews` - Get shop reviews

### Recommendation Endpoints
- `POST /api/recommend` - Generate AI recommendation
- `GET /api/user/recommendations` - Get user recommendations
- `POST /api/user/recommendations/<id>/save` - Save recommendation
- `DELETE /api/user/recommendations/<id>` - Delete recommendation

### Comparison Endpoints
- `GET /api/comparisons` - Get user comparisons
- `POST /api/comparisons/add` - Add product to comparison
- `DELETE /api/comparisons/<product_id>/remove` - Remove from comparison
- `DELETE /api/comparisons/clear` - Clear all comparisons

### Messaging Endpoints
- `POST /api/messages/send` - Send message
- `GET /api/messages/conversations` - Get conversations
- `GET /api/messages/conversation/<user_id>` - Get conversation messages
- `GET /api/messages/unread-count` - Get unread count
- `PUT /api/messages/<id>/read` - Mark message as read

### User Endpoints
- `GET /api/user/dashboard` - Get user dashboard data
- `GET /user/profile` - Get user profile
- `PUT /user/profile` - Update profile

### Shop Owner Endpoints
- `POST /shop/register` - Register shop
- `GET /shop/dashboard` - Get shop dashboard
- `GET /shop/<id>/inventory` - Get shop inventory
- `POST /shop/<id>/product` - Add product
- `PUT /shop/<id>/product/<id>` - Update product
- `DELETE /shop/<id>/product/<id>` - Delete product
- `GET /shop/<id>/orders` - Get shop orders
- `PUT /shop/<id>/order/<id>/status` - Update order status

### Admin Endpoints
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/shops` - Get all shops
- `POST /admin/shops/<id>/verify` - Verify shop
- `POST /admin/shops/<id>/reject` - Reject shop
- `GET /admin/payments` - Get all payments
- `POST /admin/payments/<id>/release` - Release payment
- `POST /admin/payments/<id>/refund` - Refund payment
- `GET /admin/analytics` - Get analytics
- `GET /admin/users` - Get all users

---

## System Features

### Real-time Features
1. **WebSocket Messaging**: Real-time bidirectional communication for messaging system
2. **Browser Notifications**: Desktop notifications for new messages
3. **Push Notifications** (Mobile): Background notifications for messages and orders
4. **Live Cart Updates**: Real-time cart synchronization
5. **Live Order Status**: Real-time order status updates

### AI & Machine Learning Features
1. **Material Recommendations**: AI-powered material recommendations based on project description
2. **Cost Estimation**: Automatic cost calculation for recommended materials
3. **Shop Optimization**: Intelligent shopping plan optimization based on location
4. **Service Recommendations**: AI-suggested services for construction projects

### Location-Based Features
1. **Nearby Shops**: Find shops based on user location
2. **Distance Calculation**: Haversine formula for accurate distance calculation
3. **Map Integration**: Google Maps integration for shop locations
4. **Location-based Sorting**: Sort products/shops by distance

### Payment Features
1. **Multiple Payment Methods**: Cash on delivery, mobile money, bank transfer
2. **Payment Escrow**: Payments held by admin until order completion
3. **Payment Release**: Admin releases payments to shop owners
4. **Refund System**: Admin processes refunds

### Security Features
1. **Authentication**: Session-based authentication for web, token-based for mobile
2. **Authorization**: Role-based access control (customer, shop_owner, admin)
3. **Shop Verification**: Admin verification system for shops
4. **Review Moderation**: Review approval system
5. **Cart Security**: Session-based cart for guests, user-based for authenticated users

### Analytics & Reporting
1. **Shop Dashboard Analytics**: Sales trends, top products, order statistics
2. **Admin Analytics**: System-wide statistics, popular products, top shops
3. **User Dashboard**: Order history, spending statistics, recommendation count
4. **Sales Charts**: Chart.js integration for visual analytics

### Data Management Features
1. **Guest Cart Sync**: Automatic cart merging on login
2. **Saved Carts**: Save and restore shopping carts
3. **Address Book**: Multiple delivery addresses per user
4. **Product Comparison**: Side-by-side product comparison
5. **Saved Recommendations**: Save AI-generated recommendations

---

## Workflows

### Complete Shopping Workflow
1. User browses/searches products
2. User adds products to cart
3. User views cart and updates quantities
4. User proceeds to checkout
5. User selects/enters delivery address
6. User selects payment method
7. System creates order(s)
8. System creates payment record(s)
9. Shop owner receives order notification
10. Shop owner updates order status
11. Order is delivered
12. Admin releases payment to shop owner
13. Customer can submit review

### Shop Registration Workflow
1. User registers as shop owner
2. User registers shop
3. Shop is created with is_verified=False
4. Admin reviews shop
5. Admin verifies/rejects shop
6. Shop owner receives notification
7. Verified shop appears in listings

### Messaging Workflow
1. User views shop/user profile
2. User clicks "Message"
3. System creates conversation (if new)
4. User sends message
5. System stores message in database
6. System emits WebSocket event to receiver
7. Receiver gets real-time notification
8. Receiver opens chat
9. System marks messages as read
10. Conversation continues

### AI Recommendation Workflow
1. User navigates to recommendations
2. User enters project description
3. User selects project type
4. System generates material recommendations
5. System calculates cost estimates
6. System finds nearby shops
7. System creates shopping plan
8. System displays recommendation
9. User can save recommendation
10. User can add recommended materials to cart

---

## Technical Implementation Notes

### Web (Flask)
- **Framework**: Flask with Blueprints for modular routing
- **Database**: SQLAlchemy ORM with PostgreSQL
- **Authentication**: Flask-Login for session management
- **Real-time**: Flask-SocketIO for WebSocket communication
- **Migrations**: Flask-Migrate (Alembic) for database migrations
- **Templates**: Jinja2 templating engine
- **Frontend**: Bootstrap 5, JavaScript, AJAX, Chart.js
- **Maps**: Google Maps JavaScript API

### Mobile (Flutter)
- **Framework**: Flutter with Dart
- **State Management**: Riverpod
- **Routing**: go_router
- **HTTP Client**: Dio
- **WebSocket**: Socket.IO client
- **Local Storage**: SharedPreferences
- **Code Generation**: Freezed, JSON Serializable
- **Architecture**: Repository pattern with providers

### Database Models
- User, Shop, Product, Service, Order, OrderItem
- Cart, CartItem, Address, Payment, Review
- Recommendation, Comparison, Message, Conversation
- Category

---

## Conclusion

This documentation covers all use cases for the BuildSmart application across both web and mobile platforms. The system supports three main user types (customers, shop owners, admins) with comprehensive features for shopping, shop management, messaging, AI recommendations, and administrative functions.

The application uses modern web technologies (Flask, WebSocket) and mobile technologies (Flutter) to provide a seamless experience across platforms with real-time features, AI-powered recommendations, and comprehensive e-commerce functionality.

