"""
Error handling utilities for BuildSmart application.
"""
from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)


def handle_api_error(error, status_code=500):
    """
    Handle API errors and return JSON response.
    
    Args:
        error: The error object or message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (JSON response, status code)
    """
    if isinstance(error, HTTPException):
        status_code = error.code
        message = error.description
    else:
        message = str(error)
    
    logger.error(f"API Error {status_code}: {message}")
    
    return jsonify({
        'error': True,
        'message': message,
        'status_code': status_code
    }), status_code


def handle_validation_error(field_errors):
    """
    Handle form validation errors.
    
    Args:
        field_errors (dict): Dictionary of field errors
        
    Returns:
        tuple: (JSON response, status code)
    """
    return jsonify({
        'error': True,
        'message': 'Validation failed',
        'field_errors': field_errors,
        'status_code': 400
    }), 400


def handle_permission_error(message="Permission denied"):
    """
    Handle permission denied errors.
    
    Args:
        message (str): Error message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return jsonify({
        'error': True,
        'message': message,
        'status_code': 403
    }), 403


def handle_not_found_error(resource="Resource"):
    """
    Handle resource not found errors.
    
    Args:
        resource (str): Name of the resource
        
    Returns:
        tuple: (JSON response, status code)
    """
    return jsonify({
        'error': True,
        'message': f"{resource} not found",
        'status_code': 404
    }), 404


def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in request data.
    
    Args:
        data (dict): Request data
        required_fields (list): List of required field names
        
    Returns:
        tuple: (is_valid, field_errors)
    """
    field_errors = {}
    
    for field in required_fields:
        if field not in data or not data[field]:
            field_errors[field] = f"{field} is required"
    
    return len(field_errors) == 0, field_errors


def validate_json_request():
    """
    Validate that request contains valid JSON.
    
    Returns:
        tuple: (is_valid, data_or_error)
    """
    if not request.is_json:
        return False, "Request must be JSON"
    
    try:
        data = request.get_json()
        if data is None:
            return False, "Invalid JSON data"
        return True, data
    except Exception as e:
        return False, f"JSON parsing error: {str(e)}"
