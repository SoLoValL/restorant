# -*- coding: utf-8 -*-
"""
Download all external media resources locally.
Usage: python download_media.py
"""
import os
import sys
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# External URLs to download
IMAGES = [
    # Dishes
    ('dishes/bruschetta-tomatoes.jpg', 'https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=600'),
    ('dishes/canapes-salmon.jpg', 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600'),
    ('dishes/olivier.jpg', 'https://images.unsplash.com/photo-1541592106381-b31e9677c0e4?w=600'),
    ('dishes/caesar-chicken.jpg', 'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=600'),
    ('dishes/greek-salad.jpg', 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600'),
    ('dishes/vitamin-salad.jpg', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600'),
    ('dishes/tom-yam.jpg', 'https://images.unsplash.com/photo-1548943487-a2e4e43b4853?w=600'),
    ('dishes/mushroom-soup.jpg', 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600'),
    ('dishes/borscht.jpg', 'https://images.unsplash.com/photo-1603105037880-880cd4f5b2d6?w=600'),
    ('dishes/ribeye-steak.jpg', 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600'),
    ('dishes/pasta-carbonara.jpg', 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600'),
    ('dishes/chicken-tikka.jpg', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600'),
    ('dishes/vegan-bowl.jpg', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600'),
    ('dishes/pizza-margarita.jpg', 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600'),
    ('dishes/pizza-pepperoni.jpg', 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600'),
    ('dishes/pizza-four-cheeses.jpg', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600'),
    ('dishes/tiramisu.jpg', 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600'),
    ('dishes/cheesecake.jpg', 'https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=600'),
    ('dishes/lemonade.jpg', 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600'),
    ('dishes/cappuccino.jpg', 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600'),
    # Blog posts
    ('blog/steaks.jpg', 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600'),
    ('blog/autumn-menu.jpg', 'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=600'),
    ('blog/wine-pairing.jpg', 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=600'),
    # Hero background
    ('hero/restaurant-interior.jpg', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1920'),
]

STATIC_FILES = [
    # Bootstrap 5.3.3
    ('bootstrap/5.3.3/css/bootstrap.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'),
    ('bootstrap/5.3.3/js/bootstrap.bundle.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'),
    # Font Awesome 6.5.0
    ('font-awesome/6.5.0/css/all.min.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'),
]


def download_file(url, filepath):
    """Download a file from URL to filepath."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  SKIP {filepath} ({size} bytes already exists)")
        return True
    
    try:
        print(f"  Downloading {filepath}...")
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath)
        print(f"  OK {filepath} ({size} bytes)")
        return True
    except Exception as e:
        print(f"  FAIL {filepath}: {e}")
        return False


def main():
    print("=" * 60)
    print("Downloading external media resources...")
    print("=" * 60)
    
    # Download images
    print("\n[1/2] Downloading images...")
    print("-" * 60)
    success = 0
    for filename, url in IMAGES:
        filepath = os.path.join(MEDIA_DIR, filename)
        if download_file(url, filepath):
            success += 1
    
    print(f"\n  Images: {success}/{len(IMAGES)} downloaded")
    
    # Download static files
    print("\n[2/2] Downloading static files...")
    print("-" * 60)
    success = 0
    for relpath, url in STATIC_FILES:
        filepath = os.path.join(STATIC_DIR, relpath)
        if download_file(url, filepath):
            success += 1
    
    print(f"\n  Static files: {success}/{len(STATIC_FILES)} downloaded")
    
    print("\n" + "=" * 60)
    print("Done! Now update templates to use local paths.")
    print("=" * 60)


if __name__ == '__main__':
    main()
