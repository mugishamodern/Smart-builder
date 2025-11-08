"""
Image processing service for product images.

This module provides image upload, validation, resizing,
and thumbnail generation functionality.
"""
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image
from flask import current_app
from app.extensions import db
from app.models import ProductImage


class ImageService:
    """Service for image processing and management"""
    
    # Allowed image extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Image dimensions
    MAIN_IMAGE_SIZE = (800, 800)
    THUMBNAIL_SIZE = (200, 200)
    
    # Image quality settings
    MAIN_IMAGE_QUALITY = 85
    THUMBNAIL_QUALITY = 75
    WEBP_QUALITY = 80
    
    # Enable WebP format for better compression
    USE_WEBP = True
    
    @staticmethod
    def allowed_file(filename):
        """
        Check if file extension is allowed.
        
        Args:
            filename (str): File name
            
        Returns:
            bool: True if allowed, False otherwise
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImageService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_image(file):
        """
        Validate image file.
        
        Args:
            file: FileStorage object
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file:
            return False, 'No file provided'
        
        if file.filename == '':
            return False, 'No file selected'
        
        if not ImageService.allowed_file(file.filename):
            return False, f'Invalid file type. Allowed types: {", ".join(ImageService.ALLOWED_EXTENSIONS)}'
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > ImageService.MAX_FILE_SIZE:
            return False, f'File too large. Maximum size: {ImageService.MAX_FILE_SIZE / (1024 * 1024)}MB'
        
        # Try to open as image to validate
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)  # Reset file pointer
            return True, None
        except Exception as e:
            return False, f'Invalid image file: {str(e)}'
    
    @staticmethod
    def resize_image(image_file, size, quality=85):
        """
        Resize image maintaining aspect ratio.
        
        Args:
            image_file: PIL Image object or file-like object
            size: Tuple (width, height)
            quality: JPEG quality (1-100)
            
        Returns:
            PIL Image: Resized image
        """
        # If it's already a PIL Image, use it directly
        if isinstance(image_file, Image.Image):
            image = image_file
        else:
            # Open and verify image
            image = Image.open(image_file)
            image.verify()
            # Reopen for processing (verify closes the image)
            image_file.seek(0)
            image = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize maintaining aspect ratio
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        return image
    
    @staticmethod
    def save_image(file, product_id, is_primary=False):
        """
        Save uploaded image and create thumbnail.
        
        Args:
            file: FileStorage object
            product_id: Product ID
            is_primary: Whether this is the primary image
            
        Returns:
            ProductImage: Created ProductImage object or None if failed
        """
        # Validate image
        is_valid, error_msg = ImageService.validate_image(file)
        if not is_valid:
            current_app.logger.error(f'Image validation failed: {error_msg}')
            return None
        
        try:
            # Generate unique filename
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            
            # Create directories
            upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'products')
            thumbnail_folder = os.path.join(upload_folder, 'thumbnails')
            
            os.makedirs(upload_folder, exist_ok=True)
            os.makedirs(thumbnail_folder, exist_ok=True)
            
            # Save main image
            file_path = os.path.join(upload_folder, unique_filename)
            thumbnail_path = os.path.join(thumbnail_folder, unique_filename)
            
            # Process and save main image
            file.seek(0)  # Reset file pointer
            img = Image.open(file)
            resized_img = ImageService.resize_image(img, ImageService.MAIN_IMAGE_SIZE)
            
            # Save as WebP if supported, otherwise JPEG
            if ImageService.USE_WEBP and ext.lower() not in ['gif']:
                # Save as WebP for better compression
                webp_filename = unique_filename.rsplit('.', 1)[0] + '.webp'
                file_path = os.path.join(upload_folder, webp_filename)
                resized_img.save(file_path, 'WEBP', quality=ImageService.WEBP_QUALITY, method=6)
                unique_filename = webp_filename
            else:
                resized_img.save(file_path, 'JPEG', quality=ImageService.MAIN_IMAGE_QUALITY, optimize=True)
            
            # Create and save thumbnail
            file.seek(0)  # Reset file pointer again
            img = Image.open(file)
            thumbnail_img = ImageService.resize_image(img, ImageService.THUMBNAIL_SIZE)
            
            # Save thumbnail as WebP if supported
            if ImageService.USE_WEBP and ext.lower() not in ['gif']:
                webp_thumbnail_filename = unique_filename.rsplit('.', 1)[0] + '_thumb.webp'
                thumbnail_path = os.path.join(thumbnail_folder, webp_thumbnail_filename)
                thumbnail_img.save(thumbnail_path, 'WEBP', quality=ImageService.WEBP_QUALITY, method=6)
            else:
                thumbnail_img.save(thumbnail_path, 'JPEG', quality=ImageService.THUMBNAIL_QUALITY, optimize=True)
            
            # Generate URLs (relative to static folder)
            image_url = f"/uploads/products/{unique_filename}"
            thumbnail_url = f"/uploads/products/thumbnails/{unique_filename}"
            
            # Create ProductImage record
            product_image = ProductImage(
                product_id=product_id,
                image_url=image_url,
                thumbnail_url=thumbnail_url,
                is_primary=is_primary,
                display_order=0
            )
            
            db.session.add(product_image)
            
            # If this is primary, unset other primary images
            if is_primary:
                ProductImage.query.filter_by(
                    product_id=product_id
                ).filter(
                    ProductImage.id != product_image.id
                ).update({'is_primary': False})
            
            db.session.commit()
            
            return product_image
            
        except Exception as e:
            current_app.logger.error(f'Error saving image: {str(e)}')
            db.session.rollback()
            return None
    
    @staticmethod
    def save_multiple_images(files, product_id):
        """
        Save multiple images for a product.
        
        Args:
            files: List of FileStorage objects
            product_id: Product ID
            
        Returns:
            list: List of created ProductImage objects
        """
        saved_images = []
        
        for i, file in enumerate(files):
            is_primary = (i == 0)  # First image is primary
            product_image = ImageService.save_image(file, product_id, is_primary=is_primary)
            
            if product_image:
                product_image.display_order = i
                db.session.commit()
                saved_images.append(product_image)
        
        return saved_images
    
    @staticmethod
    def delete_image(product_image_id):
        """
        Delete image and its files.
        
        Args:
            product_image_id: ProductImage ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            product_image = ProductImage.query.get(product_image_id)
            if not product_image:
                return False
            
            # Delete files
            upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'products')
            
            image_path = os.path.join(upload_folder, product_image.image_url.split('/')[-1])
            thumbnail_path = os.path.join(upload_folder, 'thumbnails', product_image.thumbnail_url.split('/')[-1] if product_image.thumbnail_url else '')
            
            if os.path.exists(image_path):
                os.remove(image_path)
            
            if product_image.thumbnail_url and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            
            # Delete database record
            db.session.delete(product_image)
            db.session.commit()
            
            return True
            
        except Exception as e:
            current_app.logger.error(f'Error deleting image: {str(e)}')
            db.session.rollback()
            return False

