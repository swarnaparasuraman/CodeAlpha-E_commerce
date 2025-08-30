#!/usr/bin/env python
"""
Fix specific product images: portable charger, science fiction novel, and yoga mat
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

# Better image URLs for the specific products
SPECIFIC_IMAGES = {
    'portable-charger': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop',
    'science-fiction-novel': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop',
    'yoga-mat': 'https://images.unsplash.com/photo-1506629905607-c52b1b8e8d19?w=400&h=400&fit=crop'
}

def download_image(url, max_retries=3):
    """Download image from URL with retries"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Open and resize image
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=95)
            img_io.seek(0)
            
            return img_io.getvalue()
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                # Try alternative URLs
                alt_urls = {
                    'portable-charger': [
                        'https://images.unsplash.com/photo-1609592806787-3d9c5b1b8b8e?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400&h=400&fit=crop'
                    ],
                    'science-fiction-novel': [
                        'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=400&fit=crop'
                    ],
                    'yoga-mat': [
                        'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
                        'https://images.unsplash.com/photo-1506629905607-c52b1b8e8d19?w=400&h=400&fit=crop'
                    ]
                }
                
                # Find which product this is for
                for product_slug, product_url in SPECIFIC_IMAGES.items():
                    if product_url == url and product_slug in alt_urls:
                        for alt_url in alt_urls[product_slug]:
                            try:
                                alt_response = requests.get(alt_url, headers=headers, timeout=15)
                                alt_response.raise_for_status()
                                
                                alt_img = Image.open(BytesIO(alt_response.content))
                                alt_img = alt_img.convert('RGB')
                                alt_img = alt_img.resize((400, 400), Image.Resampling.LANCZOS)
                                
                                alt_img_io = BytesIO()
                                alt_img.save(alt_img_io, format='JPEG', quality=95)
                                alt_img_io.seek(0)
                                
                                print(f"✅ Alternative URL worked: {alt_url}")
                                return alt_img_io.getvalue()
                            except:
                                continue
                
                return None
    
    return None

def main():
    print("🎯 Fixing specific product images...")
    print("📦 Target products: Portable Charger, Science Fiction Novel, Yoga Mat")
    
    # Get the specific products
    target_slugs = ['portable-charger', 'science-fiction-novel', 'yoga-mat']
    products = Product.objects.filter(slug__in=target_slugs)
    
    success_count = 0
    
    for product in products:
        print(f"\n🔧 Processing: {product.name}")
        
        # Get image URL for this product
        image_url = SPECIFIC_IMAGES.get(product.slug)
        
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
                print(f"❌ All download attempts failed for {product.name}")
        else:
            print(f"⚠️  No URL found for {product.name}")
    
    print(f"\n🎉 Process complete!")
    print(f"✅ Successfully updated: {success_count}/{len(products)} images")
    
    if success_count == len(products):
        print("🌟 All target images have been perfectly updated!")
    
    print(f"🚀 Refresh your browser to see the new images!")

if __name__ == '__main__':
    main()
