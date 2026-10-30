from PIL import Image, ImageChops
import os

def autocrop(im, fuzz=25, margin_pct=0.02, bg_color=None):
    im_rgb = im.convert('RGB')
    w, h = im_rgb.size
    
    if bg_color is None:
        # Sample edges (top, bottom, left, right)
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
        # median or average background color
        r = sorted([s[0] for s in samples])[len(samples)//2]
        g = sorted([s[1] for s in samples])[len(samples)//2]
        b = sorted([s[2] for s in samples])[len(samples)//2]
        bg_color = (r, g, b)
    
    bg = Image.new('RGB', (w, h), bg_color)
    diff = ImageChops.difference(im_rgb, bg)
    # convert to grayscale and threshold with fuzz
    gray = diff.convert('L')
    thresh = gray.point(lambda p: 255 if p > fuzz else 0)
    bbox = thresh.getbbox()
    
    if not bbox:
        return im, (0, 0, w, h), bg_color
    
    pad_x = int(w * margin_pct)
    pad_y = int(h * margin_pct)
    
    crop_x0 = max(0, bbox[0] - pad_x)
    crop_y0 = max(0, bbox[1] - pad_y)
    crop_x1 = min(w, bbox[2] + pad_x)
    crop_y1 = min(h, bbox[3] + pad_y)
    
    return im.crop((crop_x0, crop_y0, crop_x1, crop_y1)), (crop_x0, crop_y0, crop_x1, crop_y1), bg_color

test_files = [
    'images/20260608_185658.jpg',
    'images/20260608_185807.jpg',
    'images/20260610_115003.jpg',
    'images/20260610_120150.jpg',
    'images/20260610_115115.jpg',
    'images/Moodboard MD2.png'
]

for f in test_files:
    im = Image.open(f)
    cropped, bbox, bg = autocrop(im, fuzz=20, margin_pct=0.02)
    print(f'{f}: orig {im.size} -> cropped {cropped.size} (bbox={bbox}, bg={bg})')
