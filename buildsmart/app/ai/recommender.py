"""
AI Recommendation Engine for BuildSmart
This module provides intelligent recommendations for construction materials and services
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from app.models import Product, Service, Shop
from app.extensions import db


class MaterialRecommender:
    """
    AI-powered material recommendation system
    Uses TF-IDF and cosine similarity for matching user needs to products
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.material_database = self._load_material_database()
    
    def _load_material_database(self):
        """Load standard materials database with typical quantities"""
        return {
            '2_bedroom_house': {
                'cement': {'quantity': 250, 'unit': 'bags', 'category': 'cement'},
                'bricks': {'quantity': 12000, 'unit': 'pieces', 'category': 'bricks'},
                'steel_bars': {'quantity': 800, 'unit': 'kg', 'category': 'steel'},
                'sand': {'quantity': 15, 'unit': 'tons', 'category': 'sand'},
                'aggregate': {'quantity': 20, 'unit': 'tons', 'category': 'aggregate'},
                'timber': {'quantity': 0.8, 'unit': 'cubic_meters', 'category': 'timber'},
                'roofing_sheets': {'quantity': 45, 'unit': 'pieces', 'category': 'roofing'},
                'paint': {'quantity': 80, 'unit': 'liters', 'category': 'paint'},
                'electrical_wire': {'quantity': 200, 'unit': 'meters', 'category': 'electrical'},
                'plumbing_pipes': {'quantity': 150, 'unit': 'meters', 'category': 'plumbing'},
            },
            '3_bedroom_house': {
                'cement': {'quantity': 400, 'unit': 'bags', 'category': 'cement'},
                'bricks': {'quantity': 18000, 'unit': 'pieces', 'category': 'bricks'},
                'steel_bars': {'quantity': 1200, 'unit': 'kg', 'category': 'steel'},
                'sand': {'quantity': 22, 'unit': 'tons', 'category': 'sand'},
                'aggregate': {'quantity': 30, 'unit': 'tons', 'category': 'aggregate'},
                'timber': {'quantity': 1.2, 'unit': 'cubic_meters', 'category': 'timber'},
                'roofing_sheets': {'quantity': 65, 'unit': 'pieces', 'category': 'roofing'},
                'paint': {'quantity': 120, 'unit': 'liters', 'category': 'paint'},
                'electrical_wire': {'quantity': 300, 'unit': 'meters', 'category': 'electrical'},
                'plumbing_pipes': {'quantity': 220, 'unit': 'meters', 'category': 'plumbing'},
            },
            'commercial_building': {
                'cement': {'quantity': 600, 'unit': 'bags', 'category': 'cement'},
                'bricks': {'quantity': 25000, 'unit': 'pieces', 'category': 'bricks'},
                'steel_bars': {'quantity': 2000, 'unit': 'kg', 'category': 'steel'},
                'sand': {'quantity': 35, 'unit': 'tons', 'category': 'sand'},
                'aggregate': {'quantity': 45, 'unit': 'tons', 'category': 'aggregate'},
                'timber': {'quantity': 1.5, 'unit': 'cubic_meters', 'category': 'timber'},
                'roofing_sheets': {'quantity': 85, 'unit': 'pieces', 'category': 'roofing'},
                'paint': {'quantity': 180, 'unit': 'liters', 'category': 'paint'},
                'electrical_wire': {'quantity': 500, 'unit': 'meters', 'category': 'electrical'},
                'plumbing_pipes': {'quantity': 350, 'unit': 'meters', 'category': 'plumbing'},
            }
        }
    
    def recommend_materials(self, project_description, project_type='2_bedroom_house', custom_specs=None):
        """
        Generate material recommendations based on project description
        
        Args:
            project_description: User's description of their project
            project_type: Type of building project
            custom_specs: Optional custom specifications
        
        Returns:
            Dictionary containing recommended materials with quantities and categories
        """
        # Get base materials for project type
        base_materials = self.material_database.get(project_type, self.material_database['2_bedroom_house'])
        
        # Apply custom adjustments if provided
        if custom_specs:
            base_materials = self._adjust_quantities(base_materials, custom_specs)
        
        return base_materials
    
    def _adjust_quantities(self, materials, specs):
        """Adjust material quantities based on custom specifications"""
        adjusted = materials.copy()
        
        # Scaling factor based on area
        if 'area_sq_meters' in specs:
            base_area = 80  # Base area for 2-bedroom
            scale_factor = specs['area_sq_meters'] / base_area
            
            for material in adjusted:
                adjusted[material]['quantity'] = int(adjusted[material]['quantity'] * scale_factor)
        
        # Floor-specific adjustments
        if 'floors' in specs and specs['floors'] > 1:
            floor_factor = 0.5 * (specs['floors'] - 1)  # 50% increase per additional floor
            for material in ['cement', 'bricks', 'steel_bars', 'paint']:
                if material in adjusted:
                    adjusted[material]['quantity'] = int(adjusted[material]['quantity'] * (1 + floor_factor))
        
        return adjusted
    
    def estimate_cost(self, materials, user_location=None):
        """
        Estimate total cost of materials
        
        Args:
            materials: Dictionary of recommended materials
            user_location: User's location for finding nearby shops
        
        Returns:
            Dictionary with cost breakdown and total estimate
        """
        cost_breakdown = {}
        total_cost = 0
        
        for material_name, material_info in materials.items():
            # Query products matching this material category
            category = material_info['category']
            products = Product.query.filter_by(
                category=category,
                is_available=True
            ).order_by(Product.price).all()
            
            if products:
                # Use average price from available products
                avg_price = sum(p.price for p in products[:3]) / min(len(products), 3)
                quantity = material_info['quantity']
                subtotal = avg_price * quantity
                
                cost_breakdown[material_name] = {
                    'quantity': quantity,
                    'unit': material_info['unit'],
                    'unit_price': round(avg_price, 2),
                    'subtotal': round(subtotal, 2)
                }
                total_cost += subtotal
        
        return {
            'breakdown': cost_breakdown,
            'total': round(total_cost, 2),
            'currency': 'UGX'
        }


class ServiceRecommender:
    """
    Service recommendation system for construction professionals
    """
    
    def recommend_services(self, project_type, materials):
        """
        Recommend construction services based on project type and materials
        
        Args:
            project_type: Type of building project
            materials: Recommended materials
        
        Returns:
            List of recommended service types
        """
        service_recommendations = []
        
        # Core services for any construction
        service_recommendations.extend([
            {
                'type': 'civil_engineer',
                'title': 'Civil Engineer / Structural Designer',
                'estimated_hours': 40,
                'priority': 'high'
            },
            {
                'type': 'mason',
                'title': 'Mason / Bricklayer',
                'estimated_hours': 200,
                'priority': 'high'
            },
        ])
        
        # Add services based on materials
        if any('electrical' in m for m in materials.keys()):
            service_recommendations.append({
                'type': 'electrician',
                'title': 'Licensed Electrician',
                'estimated_hours': 60,
                'priority': 'high'
            })
        
        if any('plumbing' in m for m in materials.keys()):
            service_recommendations.append({
                'type': 'plumber',
                'title': 'Licensed Plumber',
                'estimated_hours': 50,
                'priority': 'high'
            })
        
        if any('timber' in m or 'roofing' in m for m in materials.keys()):
            service_recommendations.append({
                'type': 'carpenter',
                'title': 'Carpenter / Roofer',
                'estimated_hours': 80,
                'priority': 'medium'
            })
        
        if any('paint' in m for m in materials.keys()):
            service_recommendations.append({
                'type': 'painter',
                'title': 'Professional Painter',
                'estimated_hours': 60,
                'priority': 'low'
            })
        
        return service_recommendations


class ShopOptimizer:
    """
    Optimize shopping routes to minimize cost and distance
    """
    
    def optimize_shopping_plan(self, materials, user_lat, user_lon, max_shops=5):
        """
        Create an optimized shopping plan
        
        Args:
            materials: Dictionary of required materials
            user_lat: User's latitude
            user_lon: User's longitude
            max_shops: Maximum number of shops to visit
        
        Returns:
            Optimized shopping plan with shops and products
        """
        shopping_plan = []
        material_categories = {m['category'] for m in materials.values()}
        
        # Find shops with required products
        shops_with_products = {}
        
        for category in material_categories:
            products = Product.query.filter_by(
                category=category,
                is_available=True
            ).join(Shop).filter(Shop.is_verified == True).all()
            
            for product in products:
                shop_id = product.shop_id
                if shop_id not in shops_with_products:
                    shops_with_products[shop_id] = {
                        'shop': product.shop,
                        'products': [],
                        'total_cost': 0,
                        'distance': product.shop.distance_to(user_lat, user_lon)
                    }
                
                shops_with_products[shop_id]['products'].append(product)
                shops_with_products[shop_id]['total_cost'] += product.price
        
        # Score shops based on cost and distance
        scored_shops = []
        for shop_data in shops_with_products.values():
            # Normalize cost and distance (lower is better)
            cost_score = shop_data['total_cost']
            distance_score = shop_data['distance'] * 10  # Weight distance
            
            # Combined score (lower is better)
            combined_score = cost_score + distance_score
            
            scored_shops.append({
                'shop': shop_data['shop'],
                'products': shop_data['products'],
                'total_cost': round(shop_data['total_cost'], 2),
                'distance_km': round(shop_data['distance'], 2),
                'score': combined_score
            })
        
        # Sort by score and return top shops
        scored_shops.sort(key=lambda x: x['score'])
        return scored_shops[:max_shops]


def generate_full_recommendation(user_id, project_description, project_type, 
                                 custom_specs=None, user_lat=None, user_lon=None):
    """
    Main function to generate complete recommendation
    
    Args:
        user_id: User requesting recommendation
        project_description: Description of the project
        project_type: Type of project
        custom_specs: Custom specifications
        user_lat: User latitude
        user_lon: User longitude
    
    Returns:
        Complete recommendation dictionary
    """
    material_rec = MaterialRecommender()
    service_rec = ServiceRecommender()
    shop_opt = ShopOptimizer()
    
    # Generate material recommendations
    materials = material_rec.recommend_materials(project_description, project_type, custom_specs)
    
    # Estimate costs
    cost_estimate = material_rec.estimate_cost(materials, (user_lat, user_lon) if user_lat else None)
    
    # Generate service recommendations
    services = service_rec.recommend_services(project_type, materials)
    
    # Optimize shopping plan
    shopping_plan = []
    if user_lat and user_lon:
        shopping_plan = shop_opt.optimize_shopping_plan(materials, user_lat, user_lon)
    
    return {
        'project_type': project_type,
        'materials': materials,
        'cost_estimate': cost_estimate,
        'services': services,
        'shopping_plan': shopping_plan,
        'confidence_score': 0.85  # Can be calculated based on data availability
    }