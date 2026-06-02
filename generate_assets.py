import os
import sys
import subprocess

# Ensure imaging library is present
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("[Internal] Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

def create_image(filename, size, is_icon=False):
    # Deep slate/charcoal background
    bg_color = (15, 23, 42) 
    # Crisp white accent
    accent_color = (255, 255, 255) 
    
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Calculate geometric precision based on canvas size
    cx, cy = size[0]//2, size[1]//2
    r = int(min(size) * (0.35 if is_icon else 0.15))
    
    # Draw geometric abstract shape: Outer secure ring
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=accent_color, width=int(r*0.1))
    
    # Inner precision diamond
    offset = r * 0.6
    draw.polygon([
        (cx, cy - offset), 
        (cx + offset, cy), 
        (cx, cy + offset), 
        (cx - offset, cy)
    ], outline=accent_color, width=int(r*0.08))
    
    img.save(filename)
    print(f"[True] Generated secure asset: {filename}")

if __name__ == "__main__":
    # Ensure vault directory exists
    os.makedirs('vault', exist_ok=True)
    
    # Generate Kivy/Buildozer Icon (512x512)
    create_image('vault/icon.png', (512, 512), is_icon=True)
    
    # Generate Kivy/Buildozer Presplash screen (1080x1920)
    create_image('vault/presplash.png', (1080, 1920), is_icon=False)
    
    print("[True] All vault aesthetic assets generated. Ready for Buildozer.")
