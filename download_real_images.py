#!/usr/bin/env python
"""
Download real product images from the internet for each product
"""
import os
import sys
import django
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_app.settings')
django.setup()

from store.models import Product

# Real product image URLs from free image sources
PRODUCT_IMAGES = {
    'wireless-bluetooth-headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
    'smartphone-case': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=400&fit=crop',
    'portable-charger': 'https://images.unsplash.com/photo-1609592806787-3d9c5b1b8b8e?w=400&h=400&fit=crop',
    'cotton-t-shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
    'denim-jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
    'winter-jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
    'python-programming-guide': 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=400&fit=crop',
    'science-fiction-novel': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
    'led-desk-lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop',
    'plant-pot-set': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=400&fit=crop',
    'yoga-mat': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
    'water-bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop',
    'vitamin-c-serum': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop',
    'essential-oil-set': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400&h=400&fit=crop'
}

def download_image(url, max_retries=3):
    """Download image from URL with retries"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Open and resize image
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)
            img_io.seek(0)
            
            return img_io.getvalue()
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return None
    
    return None

def create_fallback_image(product_name, category_name):
    """Create fallback image if download fails"""
    colors = {
        'Electronics': '#3B82F6',
        'Clothing': '#EF4444', 
        'Books': '#10B981',
        'Home & Garden': '#F59E0B',
        'Sports & Outdoors': '#8B5CF6',
        'Health & Beauty': '#EC4899'
    }
    
    color = colors.get(category_name, '#6B7280')
    img = Image.new('RGB', (400, 400), color=color)
    
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    
    return img_io.getvalue()

def main():
    print("🖼️  Downloading real product images...")
    
    products = Product.objects.all()
    success_count = 0
    
    for product in products:
        print(f"\n📦 Processing: {product.name}")
        
        # Get image URL for this product
        image_url = PRODUCT_IMAGES.get(product.slug)
        
        if image_url:
            print(f"🌐 Downloading from: {image_url}")
            image_data = download_image(image_url)
            
            if image_data:
                # Save the downloaded image
                filename = f"{product.slug}.jpg"
                product.image.save(
                    filename,
                    ContentFile(image_data),
                    save=True
                )
                print(f"✅ Successfully saved: {filename}")
                success_count += 1
            else:
                print(f"❌ Download failed, creating fallback...")
                fallback_data = create_fallback_image(product.name, product.category.name)
                filename = f"{product.slug}.jpg"
                product.image.save(
                    filename,
                    ContentFile(fallback_data),
                    save=True
                )
                print(f"🔄 Fallback image saved: {filename}")
        else:
            print(f"⚠️  No URL found, creating fallback...")
            fallback_data = create_fallback_image(product.name, product.category.name)
            filename = f"{product.slug}.jpg"
            product.image.save(
                filename,
                ContentFile(fallback_data),
                save=True
            )
            print(f"🔄 Fallback image saved: {filename}")
    
    print(f"\n🎉 Process complete!")
    print(f"✅ Successfully downloaded: {success_count}/{len(products)} images")
    print(f"🚀 Start server: python manage.py runserver")

if __name__ == '__main__':
    main()
