#!/usr/bin/env python
"""
Replace specific product images with custom provided images
"""
import os
import sys
import django
from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import base64

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_app.settings')
django.setup()

from store.models import Product

def process_image_for_product(image_path, target_size=(400, 400)):
    """Process and resize image for product"""
    try:
        # Open and process the image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to target size
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=95)
            img_io.seek(0)
            
            return img_io.getvalue()
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def update_product_image(product_slug, image_path):
    """Update a specific product with a new image"""
    try:
        # Get the product
        product = Product.objects.get(slug=product_slug)
        
        # Process the image
        image_data = process_image_for_product(image_path)
        
        if image_data:
            # Create filename
            filename = f"{product_slug}.jpg"
            
            # Save the image to the product
            product.image.save(
                filename,
                ContentFile(image_data),
                save=True
            )
            
            print(f"✅ Successfully updated {product.name} with new image")
            return True
        else:
            print(f"❌ Failed to process image for {product.name}")
            return False
            
    except Product.DoesNotExist:
        print(f"❌ Product with slug '{product_slug}' not found")
        return False
    except Exception as e:
        print(f"❌ Error updating {product_slug}: {e}")
        return False

def find_image_file(base_name):
    """Find image file with various extensions"""
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    for ext in extensions:
        path = Path(f"{base_name}{ext}")
        if path.exists():
            return path
    return None

def main():
    print("🖼️  Replacing product images with custom images...")
    print("🔍 Scanning for image files in current directory...")

    # List all image files in current directory
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
    found_images = []
    for ext in image_extensions:
        found_images.extend(Path('.').glob(ext))

    if found_images:
        print(f"📁 Found {len(found_images)} image files:")
        for img in found_images:
            print(f"   - {img.name}")
    else:
        print("❌ No image files found in current directory")
        print("📋 Please save your images with these names:")
        print("   - portable_charger_image.png (or .jpg)")
        print("   - yoga_mat_image.png (or .jpg)")
        print("   - science_fiction_image.png (or .jpg)")
        return

    # Define the image mappings - try multiple possible names
    image_mappings = {
        'portable-charger': ['portable_charger_image', 'portable_charger', 'charger'],
        'yoga-mat': ['yoga_mat_image', 'yoga_mat', 'yoga'],
        'science-fiction-novel': ['science_fiction_image', 'science_fiction', 'books', 'novel']
    }

    success_count = 0
    total_count = len(image_mappings)

    for product_slug, possible_names in image_mappings.items():
        print(f"\n🔄 Processing {product_slug}...")

        # Try to find the image file
        image_path = None
        for name in possible_names:
            image_path = find_image_file(name)
            if image_path:
                print(f"✅ Found image: {image_path}")
                break

        if not image_path:
            print(f"⚠️  No image found for {product_slug}")
            print(f"   Tried: {', '.join([f'{name}.*' for name in possible_names])}")
            continue

        # Update the product
        if update_product_image(product_slug, image_path):
            success_count += 1

    print(f"\n🎉 Process complete!")
    print(f"✅ Successfully updated: {success_count}/{total_count} images")

    if success_count == total_count:
        print("🌟 All custom images have been perfectly applied!")
    else:
        print("⚠️  Some images were not updated. Please check the file paths.")

    print("🚀 Refresh your browser to see the new custom images!")

if __name__ == '__main__':
    main()
