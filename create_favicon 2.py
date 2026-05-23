#!/usr/bin/env python3
"""
Script to create a cannabis-themed favicon.ico file
"""

# Create a simple cannabis leaf favicon using basic ICO format
# This creates a 16x16 and 32x32 ICO file with a cannabis leaf design

import struct

def create_cannabis_favicon():
    # ICO header
    ico_header = struct.pack('<HHH', 0, 1, 2)  # Reserved, Type (1=ICO), Count (2 images)
    
    # Image directory entries for 16x16 and 32x32
    dir_entry_16 = struct.pack('<BBBBHHII', 16, 16, 0, 0, 1, 32, 0, 22)  # 16x16, 32bpp
    dir_entry_32 = struct.pack('<BBBBHHII', 32, 32, 0, 0, 1, 32, 0, 22)  # 32x32, 32bpp
    
    # Cannabis leaf pattern for 16x16 (simplified)
    # Using RGBA format (4 bytes per pixel)
    ocean_green = (13, 148, 136, 255)  # #0d9488
    white = (255, 255, 255, 255)
    transparent = (0, 0, 0, 0)
    
    # 16x16 cannabis leaf pattern
    pattern_16 = [
        [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    ]
    
    # Create the 16x16 bitmap data
    bitmap_16 = bytearray()
    for row in pattern_16:
        for pixel in row:
            if pixel == 1:
                bitmap_16.extend(ocean_green)
            else:
                bitmap_16.extend(transparent)
    
    # Create BMP header for 16x16
    bmp_header_16 = struct.pack('<IIIHHIIIIII', 
                               40,  # header size
                               16,  # width
                               32,  # height (16*2 for AND mask)
                               1,   # planes
                               32,  # bits per pixel
                               0,   # compression
                               len(bitmap_16) + 16*16//8,  # image size
                               0, 0, 0, 0)  # other fields
    
    # AND mask (transparency mask) - all transparent
    and_mask_16 = b'\x00' * (16 * 16 // 8)
    
    # Combine 16x16 data
    image_16 = bmp_header_16 + bitmap_16 + and_mask_16
    
    # Update directory entry with correct offset and size
    dir_entry_16 = struct.pack('<BBBBHHII', 16, 16, 0, 0, 1, 32, len(image_16), 22)
    
    # For simplicity, we'll duplicate the 16x16 for 32x32 (scaled)
    # In a real implementation, you'd create a proper 32x32 version
    dir_entry_32 = struct.pack('<BBBBHHII', 32, 32, 0, 0, 1, 32, len(image_16), 22 + len(image_16))
    
    # Combine everything
    ico_data = ico_header + dir_entry_16 + dir_entry_32 + image_16 + image_16
    
    return ico_data

if __name__ == "__main__":
    try:
        ico_data = create_cannabis_favicon()
        with open('/Users/uba/Desktop/hemp-app/chaos-magement/static/favicon.ico', 'wb') as f:
            f.write(ico_data)
        print("Cannabis-themed favicon.ico created successfully!")
    except Exception as e:
        print(f"Error creating favicon: {e}")
