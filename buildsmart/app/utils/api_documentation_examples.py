"""
API Documentation Examples.

This file contains examples of how to add Swagger/OpenAPI documentation
to API endpoints using flasgger decorators.

These examples can be copied to actual route files to document endpoints.
"""

# Example 1: Simple GET endpoint
"""
@api_bp.route('/shops/nearby', methods=['GET'])
@swag_from({
    'tags': ['Shops'],
    'summary': 'Get shops near a location',
    'description': 'Returns a list of shops within a specified radius of given coordinates',
    'parameters': [
        {
            'name': 'lat',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': True,
            'description': 'Latitude coordinate'
        },
        {
            'name': 'lon',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': True,
            'description': 'Longitude coordinate'
        },
        {
            'name': 'radius',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'default': 10,
            'description': 'Search radius in kilometers'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful response',
            'schema': {
                'type': 'object',
                'properties': {
                    'shops': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Shop'}
                    },
                    'count': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Invalid parameters'
        }
    }
})
def nearby_shops():
    # Implementation
    pass
"""

# Example 2: POST endpoint with request body
"""
@api_bp.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'User login',
    'description': 'Authenticate user and return session token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['username', 'password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'john_doe'
                    },
                    'password': {
                        'type': 'string',
                        'format': 'password',
                        'example': 'password123'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Login successful'},
                    'user': {'$ref': '#/definitions/User'}
                }
            }
        },
        '401': {
            'description': 'Invalid credentials'
        }
    }
})
def api_login():
    # Implementation
    pass
"""

# Example 3: GET with pagination
"""
@api_bp.route('/products/search', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'summary': 'Search products',
    'description': 'Search products with filters and pagination',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Search query'
        },
        {
            'name': 'category',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Category filter'
        },
        {
            'name': 'min_price',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Minimum price'
        },
        {
            'name': 'max_price',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Maximum price'
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'Page number'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 20,
            'description': 'Items per page'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful response',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Product'}
                    },
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer'},
                            'per_page': {'type': 'integer'},
                            'total': {'type': 'integer'},
                            'pages': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def search_products():
    # Implementation
    pass
"""

# Example 4: Authenticated endpoint
"""
@api_bp.route('/user/dashboard', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Users'],
    'summary': 'Get user dashboard',
    'description': 'Get user dashboard data including statistics and recent orders',
    'security': [
        {'SessionAuth': []},
        {'TokenAuth': []}
    ],
    'responses': {
        '200': {
            'description': 'Dashboard data',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user': {'$ref': '#/definitions/User'},
                            'stats': {
                                'type': 'object',
                                'properties': {
                                    'total_orders': {'type': 'integer'},
                                    'total_spent': {'type': 'number'},
                                    'pending_orders': {'type': 'integer'}
                                }
                            },
                            'recent_orders': {
                                'type': 'array',
                                'items': {'$ref': '#/definitions/Order'}
                            }
                        }
                    }
                }
            }
        },
        '401': {
            'description': 'Authentication required'
        }
    }
})
def get_user_dashboard():
    # Implementation
    pass
"""

# Model definitions for Swagger
SWAGGER_DEFINITIONS = {
    'User': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'username': {'type': 'string', 'example': 'john_doe'},
            'email': {'type': 'string', 'example': 'john@example.com'},
            'full_name': {'type': 'string', 'example': 'John Doe'},
            'user_type': {
                'type': 'string',
                'enum': ['customer', 'shop_owner', 'service_provider', 'admin'],
                'example': 'customer'
            },
            'phone': {'type': 'string', 'example': '+1234567890'},
            'created_at': {'type': 'string', 'format': 'date-time'}
        }
    },
    'Shop': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'name': {'type': 'string', 'example': 'ABC Hardware Store'},
            'description': {'type': 'string', 'example': 'Quality construction materials'},
            'address': {'type': 'string', 'example': '123 Main St'},
            'phone': {'type': 'string', 'example': '+1234567890'},
            'email': {'type': 'string', 'example': 'shop@example.com'},
            'latitude': {'type': 'number', 'format': 'float', 'example': 40.7128},
            'longitude': {'type': 'number', 'format': 'float', 'example': -74.0060},
            'rating': {'type': 'number', 'format': 'float', 'example': 4.5},
            'total_reviews': {'type': 'integer', 'example': 120},
            'is_verified': {'type': 'boolean', 'example': True},
            'is_active': {'type': 'boolean', 'example': True}
        }
    },
    'Product': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'name': {'type': 'string', 'example': 'Cement 50kg'},
            'description': {'type': 'string', 'example': 'High quality cement'},
            'price': {'type': 'number', 'format': 'float', 'example': 5000.00},
            'stock_quantity': {'type': 'integer', 'example': 100},
            'category': {'type': 'string', 'example': 'Building Materials'},
            'shop_id': {'type': 'integer', 'example': 1},
            'is_available': {'type': 'boolean', 'example': True}
        }
    },
    'Order': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'order_number': {'type': 'string', 'example': 'ORD001'},
            'customer_id': {'type': 'integer', 'example': 1},
            'shop_id': {'type': 'integer', 'example': 1},
            'total_amount': {'type': 'number', 'format': 'float', 'example': 10000.00},
            'status': {
                'type': 'string',
                'enum': ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'],
                'example': 'pending'
            },
            'payment_status': {
                'type': 'string',
                'enum': ['pending', 'paid', 'failed', 'refunded'],
                'example': 'paid'
            },
            'delivery_address': {'type': 'string', 'example': '123 Main St'},
            'created_at': {'type': 'string', 'format': 'date-time'}
        }
    }
}

