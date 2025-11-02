# API Contract (Inferred from Flask Backend)

Base URL: `${API_BASE_URL}`
Auth: Session/cookie or token-based (TBD). For mobile, prefer token-based.

## Auth
- POST /auth/login
- POST /auth/register
- POST /auth/logout

## Users
- GET /user/dashboard (stats)
- GET /user/orders
- GET /user/recommendations

## Shops
- GET /shops/nearby?lat=..&lon=..&radius=..
- GET /shop/{shop_id}/products
- GET /shops (search/filter)
- Owner endpoints (TBD): create/update shop, inventory CRUD

## Products
- GET /products (search/filter)
- GET /product/{id}

## Services
- GET /services (search/filter)
- GET /service/{id}

## Orders
- GET /orders (user)
- POST /orders (create/cart/checkout)
- GET /orders/{id}
- PATCH /orders/{id} (status) [owner/admin]

## Recommendations (AI)
- POST /api/recommend { project_description, project_type, custom_specs }

Notes:
- Confirm authentication mechanism for mobile (token vs cookie).
- Align request/response shapes with backend.
- Add error model and pagination parameters.
