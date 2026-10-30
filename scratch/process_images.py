import os, sys
from PIL import Image, ImageChops
import fitz # PyMuPDF

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def autocrop_image(im, fuzz=20, margin_pct=0.02, bg_color=None):
    im_rgb = im.convert('RGB')
    w, h = im_rgb.size
    
    if bg_color is None:
        samples = [
            im_rgb.getpixel((5, 5)),
            im_rgb.getpixel((w-6, 5)),
            im_rgb.getpixel((5, h-6)),
            im_rgb.getpixel((w-6, h-6)),
            im_rgb.getpixel((w//2, 5)),
            im_rgb.getpixel((w//2, h-6)),
            im_rgb.getpixel((5, h//2)),
            im_rgb.getpixel((w-6, h//2)),
        ]
        r = sorted([s[0] for s in samples])[len(samples)//2]
        g = sorted([s[1] for s in samples])[len(samples)//2]
        b = sorted([s[2] for s in samples])[len(samples)//2]
        bg_color = (r, g, b)
    
    bg = Image.new('RGB', (w, h), bg_color)
    diff = ImageChops.difference(im_rgb, bg)
    gray = diff.convert('L')
    thresh = gray.point(lambda p: 255 if p > fuzz else 0)
    bbox = thresh.getbbox()
    
    if not bbox:
        return im, (0, 0, w, h)
    
    pad_x = int(w * margin_pct)
    pad_y = int(h * margin_pct)
    
    crop_x0 = max(0, bbox[0] - pad_x)
    crop_y0 = max(0, bbox[1] - pad_y)
    crop_x1 = min(w, bbox[2] + pad_x)
    crop_y1 = min(h, bbox[3] + pad_y)
    
    return im.crop((crop_x0, crop_y0, crop_x1, crop_y1)), (crop_x0, crop_y0, crop_x1, crop_y1)

def export_image(im, base_path_no_ext, max_dim=1800, quality=90):
    w, h = im.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Save webp
    webp_path = base_path_no_ext + '.webp'
    jpg_path = base_path_no_ext + '.jpg'
    ensure_dir(webp_path)
    
    im_rgb = im.convert('RGB')
    im_rgb.save(webp_path, 'WEBP', quality=quality)
    im_rgb.save(jpg_path, 'JPEG', quality=quality)
    print(f'Exported: {webp_path} ({im.width}x{im.height})')
    return im.width, im.height

print("Helper functions defined successfully")
