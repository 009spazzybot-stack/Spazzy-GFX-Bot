"""
Utility functions for template management
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json

TEMPLATES_DIR = "templates"
FONTS_DIR = "fonts"
CONFIG_FILE = "config.json"


def load_config():
    """Load configuration from config.json"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_font(font_name="arial.ttf", size=40):
    """Get font from fonts folder or system"""
    # Try fonts folder first
    font_path = os.path.join(FONTS_DIR, font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass
    
    # Try system fonts
    try:
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()


def load_template(template_name):
    """Load template image from templates folder"""
    template_path = os.path.join(TEMPLATES_DIR, f"{template_name}.png")
    if os.path.exists(template_path):
        return Image.open(template_path)
    return None


def add_text_centered(img, text, position, font_size=40, color=(255, 255, 255), font_name="arial.ttf"):
    """Add centered text to image"""
    draw = ImageDraw.Draw(img)
    font = get_font(font_name, font_size)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x, y = position
    x = x - text_width // 2
    y = y - text_height // 2
    
    draw.text((x, y), text, fill=color, font=font)
    return img


def create_colored_gradient_bg(width, height, color_hex="#FF3232"):
    """Create a gradient background with specified color"""
    # Convert hex to RGB
    color_hex = color_hex.lstrip('#')
    r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    
    img = Image.new('RGB', (width, height), color=(20, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for i in range(0, width, 50):
        alpha = int(255 * (i / width))
        gradient_color = (
            min(r + alpha // 5, 255),
            min(g, 255),
            min(b, 255)
        )
        draw.rectangle([i, 0, i + 50, height], fill=gradient_color)
    
    return img


def export_graphic(img, filename, output_dir="renders"):
    """Export graphic to file"""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    img.save(output_path, format="PNG")
    return output_path


# Example usage:
# from utils import load_template, add_text_centered, export_graphic
# img = load_template("welcome")
# if img:
#     img = add_text_centered(img, "Welcome Joshua", (960, 500))
#     export_graphic(img, "welcome_joshua.png")
