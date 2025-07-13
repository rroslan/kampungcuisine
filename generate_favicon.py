#!/usr/bin/env python
"""
Favicon Generator Script for Kampung Cuisine
Generates favicon files in multiple formats from SVG source.
"""

import os
import sys
from pathlib import Path

def create_simple_favicon_ico():
    """Create a simple text-based favicon.ico file"""

    # Simple 16x16 ICO file header and data for a basic favicon
    # This creates a minimal favicon with "KC" text
    ico_data = bytearray([
        # ICO header
        0x00, 0x00,  # Reserved (must be 0)
        0x01, 0x00,  # Image type (1 = ICO)
        0x01, 0x00,  # Number of images

        # Image directory entry
        0x10,        # Width (16)
        0x10,        # Height (16)
        0x00,        # Color count (0 = no palette)
        0x00,        # Reserved
        0x01, 0x00,  # Color planes
        0x20, 0x00,  # Bits per pixel (32)
        0x68, 0x05, 0x00, 0x00,  # Size of image data
        0x16, 0x00, 0x00, 0x00,  # Offset to image data

        # BMP header
        0x28, 0x00, 0x00, 0x00,  # Size of header
        0x10, 0x00, 0x00, 0x00,  # Width
        0x20, 0x00, 0x00, 0x00,  # Height (doubled for ICO)
        0x01, 0x00,              # Planes
        0x20, 0x00,              # Bits per pixel
        0x00, 0x00, 0x00, 0x00,  # Compression
        0x00, 0x05, 0x00, 0x00,  # Image size
        0x00, 0x00, 0x00, 0x00,  # X pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Y pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Colors used
        0x00, 0x00, 0x00, 0x00,  # Important colors
    ])

    # Create a simple orange bowl pattern (16x16 pixels)
    # Each pixel is 4 bytes (BGRA format)
    pixels = []

    for y in range(16):
        for x in range(16):
            # Create a simple bowl shape
            center_x, center_y = 8, 8
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

            if distance < 6:  # Inside bowl
                if y > center_y:  # Bottom half
                    # Orange bowl color
                    pixels.extend([0x16, 0x73, 0xF9, 0xFF])  # BGRA: Orange
                else:  # Top half
                    # Lighter orange for noodles
                    pixels.extend([0x24, 0xBF, 0xFB, 0xFF])  # BGRA: Light orange
            else:
                # Transparent background
                pixels.extend([0x00, 0x00, 0x00, 0x00])  # BGRA: Transparent

    # Reverse row order (BMP stores bottom-up)
    reversed_pixels = []
    for row in range(15, -1, -1):
        start = row * 16 * 4
        end = start + 16 * 4
        reversed_pixels.extend(pixels[start:end])

    # Add AND mask (all transparent)
    and_mask = [0x00] * (16 * 2)  # 16 rows * 2 bytes per row

    ico_data.extend(reversed_pixels)
    ico_data.extend(and_mask)

    return bytes(ico_data)

def create_webapp_manifest():
    """Create a web app manifest for PWA favicon support"""
    manifest = {
        "name": "Kampung Cuisine",
        "short_name": "KC",
        "description": "Authentic Malaysian cuisine ingredients and spices",
        "theme_color": "#f97316",
        "background_color": "#ffffff",
        "display": "standalone",
        "icons": [
            {
                "src": "/static/images/favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml"
            }
        ]
    }

    import json
    return json.dumps(manifest, indent=2)

def main():
    """Generate favicon files"""
    print("🍜 Kampung Cuisine Favicon Generator")
    print("=" * 40)

    # Get script directory
    script_dir = Path(__file__).parent
    static_dir = script_dir / "static" / "images"

    # Ensure static directory exists
    static_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Creating favicon files in: {static_dir}")

    # 1. Generate favicon.ico
    print("🔨 Generating favicon.ico...")
    favicon_ico = create_simple_favicon_ico()

    ico_path = static_dir / "favicon.ico"
    with open(ico_path, "wb") as f:
        f.write(favicon_ico)
    print(f"✅ Created: {ico_path}")

    # 2. Create web app manifest
    print("📄 Generating manifest.json...")
    manifest_content = create_webapp_manifest()

    manifest_path = script_dir / "static" / "manifest.json"
    with open(manifest_path, "w") as f:
        f.write(manifest_content)
    print(f"✅ Created: {manifest_path}")

    # 3. Create Apple touch icon (simple SVG copy)
    print("🍎 Creating Apple touch icon...")
    svg_path = static_dir / "favicon.svg"
    apple_icon_path = static_dir / "apple-touch-icon.svg"

    if svg_path.exists():
        import shutil
        shutil.copy2(svg_path, apple_icon_path)
        print(f"✅ Created: {apple_icon_path}")
    else:
        print("⚠️  favicon.svg not found, skipping Apple touch icon")

    print("\n🎉 Favicon generation complete!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py collectstatic")
    print("2. Add favicon links to base.html template")
    print("3. Test in browser")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
