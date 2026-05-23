#!/usr/bin/env python3
"""
Create a better cannabis-themed favicon using PIL if available, 
otherwise use a simpler approach
"""

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_simple_cannabis_favicon():
    """Create a simple cannabis favicon without PIL"""
    # Simple SVG that browsers can use as favicon
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
  <rect width="16" height="16" fill="#0d9488" rx="2"/>
  <g fill="#ffffff" opacity="0.9">
    <!-- Simple cannabis leaf shape -->
    <path d="M8 2C7 3 6 4 5 6C4 7 4 8 5 9C6 10 7 11 8 12C9 11 10 10 11 9C12 8 12 7 11 6C10 4 9 3 8 2Z"/>
    <!-- Center vein -->
    <line x1="8" y1="2" x2="8" y2="12" stroke="#0d9488" stroke-width="0.5" opacity="0.7"/>
    <!-- Side veins -->
    <line x1="8" y1="5" x2="6" y2="7" stroke="#0d9488" stroke-width="0.3" opacity="0.6"/>
    <line x1="8" y1="5" x2="10" y2="7" stroke="#0d9488" stroke-width="0.3" opacity="0.6"/>
    <line x1="8" y1="8" x2="6" y2="10" stroke="#0d9488" stroke-width="0.3" opacity="0.6"/>
    <line x1="8" y1="8" x2="10" y2="10" stroke="#0d9488" stroke-width="0.3" opacity="0.6"/>
    <!-- Stem -->
    <rect x="7.5" y="12" width="1" height="2" fill="#ffffff" opacity="0.8"/>
  </g>
</svg>'''
    
    with open('/Users/uba/Desktop/hemp-app/chaos-magement/static/favicon-16.svg', 'w') as f:
        f.write(svg_content)
    
    print("Simple cannabis favicon created!")

def create_pil_favicon():
    """Create favicon using PIL if available"""
    if not PIL_AVAILABLE:
        return False
        
    # Create 32x32 image
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Ocean green background circle
    ocean_green = (13, 148, 136, 255)
    white = (255, 255, 255, 230)
    
    # Background circle
    draw.ellipse([2, 2, size-2, size-2], fill=ocean_green)
    
    # Cannabis leaf shape (simplified)
    center_x, center_y = size // 2, size // 2
    
    # Main leaf body
    leaf_points = [
        (center_x, center_y - 10),      # top
        (center_x - 4, center_y - 6),  # left upper
        (center_x - 6, center_y - 2),  # left middle
        (center_x - 4, center_y + 2),  # left lower
        (center_x, center_y + 8),      # bottom
        (center_x + 4, center_y + 2),  # right lower
        (center_x + 6, center_y - 2),  # right middle
        (center_x + 4, center_y - 6),  # right upper
    ]
    
    draw.polygon(leaf_points, fill=white)
    
    # Side leaflets
    left_leaflet = [(center_x - 8, center_y - 3), (center_x - 6, center_y - 6), 
                   (center_x - 4, center_y - 2), (center_x - 6, center_y + 1)]
    right_leaflet = [(center_x + 8, center_y - 3), (center_x + 6, center_y - 6), 
                    (center_x + 4, center_y - 2), (center_x + 6, center_y + 1)]
    
    draw.polygon(left_leaflet, fill=white)
    draw.polygon(right_leaflet, fill=white)
    
    # Center vein
    draw.line([(center_x, center_y - 10), (center_x, center_y + 8)], fill=ocean_green, width=1)
    
    # Save as ICO and PNG
    img.save('/Users/uba/Desktop/hemp-app/chaos-magement/static/favicon.ico', format='ICO', sizes=[(16,16), (32,32)])
    img.save('/Users/uba/Desktop/hemp-app/chaos-magement/static/favicon.png', format='PNG')
    
    return True

if __name__ == "__main__":
    if create_pil_favicon():
        print("High-quality cannabis favicon created with PIL!")
    else:
        create_simple_cannabis_favicon()
        print("Simple cannabis favicon created (install Pillow for better quality)")
