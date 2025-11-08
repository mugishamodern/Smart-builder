"""
API Documentation utilities and schemas.

This module provides schemas and utilities for API documentation
using OpenAPI/Swagger specification.
"""
from typing import Dict, Any, List, Optional


# Common API response schemas
API_RESPONSES = {
    'success': {
        'type': 'object',
        'properties': {
            'success': {'type': 'boolean', 'example': True},
            'data': {'type': 'object'},
            'message': {'type': 'string'}
        }
    },
    'error': {
        'type': 'object',
        'properties': {
            'success': {'type': 'boolean', 'example': False},
            'error': {'type': 'string'},
            'message': {'type': 'string'}
        }
    },
    'pagination': {
        'type': 'object',
        'properties': {
            'success': {'type': 'boolean', 'example': True},
            'data': {'type': 'array'},
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


# Common parameter definitions
QUERY_PARAMS = {
    'page': {
        'name': 'page',
        'in': 'query',
        'type': 'integer',
        'description': 'Page number (1-indexed)',
        'default': 1,
        'required': False
    },
    'per_page': {
        'name': 'per_page',
        'in': 'query',
        'type': 'integer',
        'description': 'Number of items per page',
        'default': 20,
        'required': False
    },
    'limit': {
        'name': 'limit',
        'in': 'query',
        'type': 'integer',
        'description': 'Maximum number of results',
        'default': 20,
        'required': False
    },
    'offset': {
        'name': 'offset',
        'in': 'query',
        'type': 'integer',
        'description': 'Number of results to skip',
        'default': 0,
        'required': False
    }
}


# Model schemas
MODEL_SCHEMAS = {
    'User': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'username': {'type': 'string', 'example': 'john_doe'},
            'email': {'type': 'string', 'example': 'john@example.com'},
            'full_name': {'type': 'string', 'example': 'John Doe'},
            'user_type': {'type': 'string', 'enum': ['customer', 'shop_owner', 'service_provider', 'admin']},
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
            'status': {'type': 'string', 'example': 'pending'},
            'payment_status': {'type': 'string', 'example': 'paid'},
            'delivery_address': {'type': 'string', 'example': '123 Main St'},
            'created_at': {'type': 'string', 'format': 'date-time'}
        }
    }
}


def get_swagger_config() -> Dict[str, Any]:
    """
    Get Swagger configuration.
    
    Returns:
        Dictionary with Swagger configuration
    """
    return {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/api/docs',
        'title': 'BuildSmart API Documentation',
        'version': '1.0.0',
        'description': """
        BuildSmart API Documentation
        
        This API provides endpoints for:
        - User authentication and management
        - Shop management
        - Product catalog and search
        - Order processing
        - Payments and financials
        - Analytics and reporting
        - Messaging and notifications
        
        ## Authentication
        
        Most endpoints require authentication. Use one of the following methods:
        
        1. **Session-based** (Web): Login via `/auth/login` to establish a session
        2. **Token-based** (Mobile/API): Use the token from `/api/auth/login`
        
        ## Rate Limiting
        
        API requests are rate limited to prevent abuse:
        - General endpoints: 200 requests per day, 50 per hour
        - Authentication endpoints: 5 per minute
        - Registration: 3 per hour
        
        ## Error Responses
        
        All error responses follow this format:
        ```json
        {
            "success": false,
            "error": "Error type",
            "message": "Error description"
        }
        ```
        
        ## Success Responses
        
        Success responses follow this format:
        ```json
        {
            "success": true,
            "data": {...},
            "message": "Optional message"
        }
        ```
        """,
        'termsOfService': 'https://buildsmart.com/terms',
        'contact': {
            'name': 'BuildSmart API Support',
            'email': 'api@buildsmart.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        },
        'tags': [
            {
                'name': 'Authentication',
                'description': 'User authentication and authorization'
            },
            {
                'name': 'Shops',
                'description': 'Shop management and search'
            },
            {
                'name': 'Products',
                'description': 'Product catalog and search'
            },
            {
                'name': 'Orders',
                'description': 'Order management and tracking'
            },
            {
                'name': 'Payments',
                'description': 'Payment processing and financials'
            },
            {
                'name': 'Analytics',
                'description': 'Analytics and reporting'
            },
            {
                'name': 'Users',
                'description': 'User management'
            },
            {
                'name': 'Search',
                'description': 'Search functionality'
            }
        ]
    }


def get_swagger_template() -> Dict[str, Any]:
    """
    Get Swagger UI template configuration.
    
    Returns:
        Dictionary with Swagger UI template configuration
    """
    return {
        'swagger': '2.0',
        'info': {
            'title': 'BuildSmart API',
            'version': '1.0.0',
            'description': 'BuildSmart Construction Marketplace API'
        },
        'host': 'localhost:5000',
        'basePath': '/api',
        'schemes': ['http', 'https'],
        'securityDefinitions': {
            'SessionAuth': {
                'type': 'apiKey',
                'name': 'session',
                'in': 'cookie',
                'description': 'Session-based authentication (web)'
            },
            'TokenAuth': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Token-based authentication (mobile/API). Format: Bearer <token>'
            }
        },
        'security': [
            {'SessionAuth': []},
            {'TokenAuth': []}
        ]
    }

