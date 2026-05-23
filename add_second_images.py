#!/usr/bin/env python
"""
Script to add placeholder second images to demonstrate carousel functionality
"""

import os
import sys
import django
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageDraw, ImageFont
import io

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Product

def create_placeholder_image(text, color='#10b981', size=(400, 400)):
    """Create a placeholder image with text"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
        except:
            font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='white', font=font)
    
    # Save to BytesIO
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    
    return buffer

def add_second_images():
    """Add second images to products for carousel demonstration"""
    products = Product.objects.all()[:10]  # First 10 products
    
    colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6b7280']
    
    for i, product in enumerate(products):
        if not product.image2:
            color = colors[i % len(colors)]
            text = f"{product.name}\nImage 2"
            
            # Create placeholder image
            image_buffer = create_placeholder_image(text, color)
            
            # Create filename
            filename = f"placeholder_image2_{product.id}.jpg"
            
            # Save image
            image_file = ContentFile(image_buffer.read(), name=filename)
            product.image2.save(filename, image_file, save=True)
            
            print(f"Added second image to: {product.name}")
        else:
            print(f"Second image already exists for: {product.name}")

def main():
    print("🖼️ Adding second images to products for carousel demonstration")
    print("=" * 60)
    
    add_second_images()
    
    print("\n✅ Second images added successfully!")
    print("You can now view the carousel functionality in the product info modal.")
    print("Click the info icon (i) on any product to see the carousel in action!")

if __name__ == "__main__":
    main()
