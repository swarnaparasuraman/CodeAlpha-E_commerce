#!/usr/bin/env python
"""
Quick script to fix product images by creating better placeholder images
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_app.settings')
django.setup()

from store.models import Product
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile

def create_product_image(product_name, category_name, width=400, height=400):
    """Create a better placeholder image with text"""
    
    # Category colors
    colors = {
        'Electronics': '#3B82F6',
        'Clothing': '#EF4444', 
        'Books': '#10B981',
        'Home & Garden': '#F59E0B',
        'Sports & Outdoors': '#8B5CF6',
        'Health & Beauty': '#EC4899'
    }
    
    color = colors.get(category_name, '#6B7280')
    
    # Create image
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add white text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Add product name text
    text_lines = product_name.split()
    if len(text_lines) > 2:
        text = '\n'.join([' '.join(text_lines[:2]), ' '.join(text_lines[2:])])
    else:
        text = product_name
    
    # Calculate text position
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 6
        text_height = 20
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with shadow
    draw.text((x+2, y+2), text, fill='black', font=font, align='center')
    draw.text((x, y), text, fill='white', font=font, align='center')
    
    return img

def main():
    print("🔧 Fixing product images...")
    
    # Get all products
    products = Product.objects.all()
    
    for product in products:
        print(f"Creating image for: {product.name}")
        
        # Create new image
        img = create_product_image(product.name, product.category.name)
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        
        # Create filename
        filename = f"{product.slug}.jpg"
        
        # Save to product
        product.image.save(
            filename,
            ContentFile(img_io.getvalue()),
            save=True
        )
        
        print(f"✅ Saved image: {filename}")
    
    print("🎉 All product images have been created!")
    print("🚀 Now start the server with: python manage.py runserver")

if __name__ == '__main__':
    main()
