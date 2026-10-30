import os, sys
from PIL import Image, ImageChops
import fitz

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
    
    webp_path = base_path_no_ext + '.webp'
    jpg_path = base_path_no_ext + '.jpg'
    ensure_dir(webp_path)
    
    im_rgb = im.convert('RGB')
    im_rgb.save(webp_path, 'WEBP', quality=quality)
    im_rgb.save(jpg_path, 'JPEG', quality=quality)
    print(f'Exported: {webp_path} ({im.width}x{im.height})')
    return im.width, im.height

dimensions = {}

# 1. 4:3 Card Crops
print("--- Generating 4:3 Card Crops ---")
# Sieraden
im_sieraden = Image.open('images/smeltende_sieraden03.png').convert('RGB')
card_sieraden = im_sieraden.crop((60, 420, 2193, 2020)).resize((1200, 900), Image.Resampling.LANCZOS)
dimensions['card_sieraden'] = export_image(card_sieraden, 'images/projecten/smeltende-sieraden/smeltende-sieraden-card')

# Stop
im_stop = Image.open('images/projecten/stop/stop-poster-definitief.webp').convert('RGB')
card_stop = im_stop.crop((0, 200, 1800, 1550)).resize((1200, 900), Image.Resampling.LANCZOS)
dimensions['card_stop'] = export_image(card_stop, 'images/projecten/stop/stop-card')

# Your Bubble
im_can = Image.open('images/Can_03.png').convert('RGB')
card_can = im_can.crop((1100, 250, 4700, 2950)).resize((1200, 900), Image.Resampling.LANCZOS)
dimensions['card_can'] = export_image(card_can, 'images/projecten/your-bubble/your-bubble-card')

# Whiplash
im_whip = Image.open('video/whiplash_poster.webp').convert('RGB')
card_whip = im_whip.crop((240, 0, 1680, 1080)).resize((1200, 900), Image.Resampling.LANCZOS)
dimensions['card_whip'] = export_image(card_whip, 'images/projecten/whiplash/whiplash-card')


# 2. Your Bubble Originals
print("--- Generating Your Bubble Images ---")
# Can_03 Mockup (Option A 4:3 composition)
can_mockup = im_can.crop((1100, 250, 4700, 2950))
dimensions['can_mockup'] = export_image(can_mockup, 'images/projecten/your-bubble/your-bubble-blik-mockup', max_dim=1800)

# Blikwrap PDF (up to 2400px wide)
doc_blik = fitz.open('images/FeevanDortmont_Drukwerk_Blikje2.pdf')
page_blik = doc_blik[0]
zoom_blik = 2400.0 / page_blik.rect.width
pix_blik = page_blik.get_pixmap(matrix=fitz.Matrix(zoom_blik, zoom_blik), alpha=False)
im_blik = Image.frombytes("RGB", [pix_blik.width, pix_blik.height], pix_blik.samples)
dimensions['blikwrap'] = export_image(im_blik, 'images/projecten/your-bubble/your-bubble-blik-wrap', max_dim=2400)

# 185658: schetsencollage
im_185658 = Image.open('images/20260608_185658.jpg')
crop_185658, _ = autocrop_image(im_185658, fuzz=20, margin_pct=0.02)
dimensions['schetsencollage'] = export_image(crop_185658, 'images/projecten/your-bubble/your-bubble-stap1-schetsencollage', max_dim=1800)

# 185807: uitgewerkte schetsen vuur en bubbels
im_185807 = Image.open('images/20260608_185807.jpg')
crop_185807, _ = autocrop_image(im_185807, fuzz=20, margin_pct=0.02)
dimensions['schetsen_vuur_bubbels'] = export_image(crop_185807, 'images/projecten/your-bubble/your-bubble-stap1-schetsen-vuur-bubbels', max_dim=1800)

# Moodboard MD2
im_mb = Image.open('images/Moodboard MD2.png')
# crop out 35px black edge
crop_mb = im_mb.crop((36, 35, 805, 1190))
dimensions['moodboard'] = export_image(crop_mb, 'images/projecten/your-bubble/your-bubble-stap2-moodboard', max_dim=1800)

# 115115: vier blikschetsen met groene stippen
im_115115 = Image.open('images/20260610_115115.jpg')
crop_115115, _ = autocrop_image(im_115115, fuzz=25, margin_pct=0.02)
dimensions['schetsen_vier_blikken'] = export_image(crop_115115, 'images/projecten/your-bubble/your-bubble-stap3-schetsen-vier-blikken', max_dim=1800)

# 115003: gekozen blikje voorkant en achterkant (gesplitst zodat ze naast elkaar passen)
im_115003 = Image.open('images/20260610_115003.jpg')
crop_voor = im_115003.crop((0, 0, im_115003.width, 1360))
crop_voor_auto, _ = autocrop_image(crop_voor, fuzz=20, margin_pct=0.02)
dimensions['blik_voor'] = export_image(crop_voor_auto, 'images/projecten/your-bubble/your-bubble-stap3-gekozen-blik-voor', max_dim=1200)

crop_achter = im_115003.crop((0, 1360, im_115003.width, im_115003.height))
crop_achter_auto, _ = autocrop_image(crop_achter, fuzz=20, margin_pct=0.02)
dimensions['blik_achter'] = export_image(crop_achter_auto, 'images/projecten/your-bubble/your-bubble-stap3-gekozen-blik-achter', max_dim=1200)


# 3. Discursive Posters voor Smeltende Sieraden
print("--- Generating Discursive Posters ---")
doc_disc = fitz.open('images/Discursive Posters.pdf')
# Page 0: Deconstructie (up to 2400px height)
p0 = doc_disc[0]
zoom0 = 2400.0 / p0.rect.height
pix0 = p0.get_pixmap(matrix=fitz.Matrix(zoom0, zoom0), alpha=False)
im_p0 = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
dimensions['poster_deconstructie'] = export_image(im_p0, 'images/projecten/smeltende-sieraden/smeltende-sieraden-poster-deconstructie', max_dim=2400)

# Page 1: Positionering (up to 2400px height)
p1 = doc_disc[1]
zoom1 = 2400.0 / p1.rect.height
pix1 = p1.get_pixmap(matrix=fitz.Matrix(zoom1, zoom1), alpha=False)
im_p1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
dimensions['poster_positionering'] = export_image(im_p1, 'images/projecten/smeltende-sieraden/smeltende-sieraden-poster-positionering', max_dim=2400)


# 4. Smeltende Sieraden foto's autocrop
print("--- Generating Smeltende Sieraden Photos ---")
# 01 and 03 (Hand sculpture)
# Hand is at y=420..3150, x=150..2150 in 2252x3533
crop_hand = im_sieraden.crop((100, 380, 2180, 3200))
dimensions['sieraden01'] = export_image(crop_hand, 'images/projecten/smeltende-sieraden/smeltende_sieraden01', max_dim=1800)
dimensions['sieraden03'] = export_image(crop_hand, 'images/projecten/smeltende-sieraden/smeltende_sieraden03', max_dim=1800)

# 02 and 04 (Six rings on mirror)
# Rings are at y=1750..2980, x=100..2000 in 2104x3317
im_rings = Image.open('images/smeltende_sieraden02.png').convert('RGB')
crop_rings = im_rings.crop((80, 1650, 2020, 3050))
dimensions['sieraden02'] = export_image(crop_rings, 'images/projecten/smeltende-sieraden/smeltende_sieraden02', max_dim=1800)
dimensions['sieraden04'] = export_image(crop_rings, 'images/projecten/smeltende-sieraden/smeltende_sieraden04', max_dim=1800)


# 5. Stop Project Images Autocrop
print("--- Autocropping Stop Images ---")
stop_files = [
    ('images/projecten/stop/stop-mindmap', 'images/projecten/stop/stop-mindmap.jpg'),
    ('images/projecten/stop/stop-stap1-mindmap', 'images/projecten/stop/stop-stap1-mindmap.jpg'),
    ('images/projecten/stop/stop-stap2-tekst-vs-beeld', 'images/projecten/stop/stop-stap2-tekst-vs-beeld.jpg'),
    ('images/projecten/stop/stop-stap2-schetsen-beeld', 'images/projecten/stop/stop-stap2-schetsen-beeld.jpg'),
    ('images/projecten/stop/stop-stap3-ai-verkenning', 'images/projecten/stop/stop-stap3-ai-verkenning.jpg'),
    ('images/projecten/stop/stop-stap4-formuleren-posters', 'images/projecten/stop/stop-stap4-formuleren-posters.jpg'),
    ('images/projecten/stop/stop-stap5-experimenteren-schetsen', 'images/projecten/stop/stop-stap5-experimenteren-schetsen.jpg'),
    ('images/projecten/stop/stop-stap6-kleur-iteraties', 'images/projecten/stop/stop-stap6-kleur-iteraties.jpg'),
    ('images/projecten/stop/stop-stap6-definitieve-opbouw', 'images/projecten/stop/stop-stap6-definitieve-opbouw.jpg'),
]

for base_out, orig_f in stop_files:
    if os.path.exists(orig_f):
        im_s = Image.open(orig_f)
        cropped, _ = autocrop_image(im_s, fuzz=20, margin_pct=0.02)
        dimensions[os.path.basename(base_out)] = export_image(cropped, base_out, max_dim=1800)

# Stop poster definitief (up to 2400px height)
if os.path.exists('images/projecten/stop/stop-poster-definitief.jpg'):
    im_p = Image.open('images/projecten/stop/stop-poster-definitief.jpg')
    cropped_p, _ = autocrop_image(im_p, fuzz=20, margin_pct=0.02)
    dimensions['stop-poster-definitief'] = export_image(cropped_p, 'images/projecten/stop/stop-poster-definitief', max_dim=2400)


# 6. Whiplash Images Autocrop
print("--- Autocropping Whiplash Images ---")
whip_files = [
    ('images/projecten/whiplash/whiplash-stap1-mindmap', 'images/projecten/whiplash/whiplash-stap1-mindmap.jpg'),
    ('images/projecten/whiplash/whiplash-stap2-storyboard', 'images/projecten/whiplash/whiplash-stap2-storyboard.jpg'),
]

for base_out, orig_f in whip_files:
    if os.path.exists(orig_f):
        im_w = Image.open(orig_f)
        cropped, _ = autocrop_image(im_w, fuzz=20, margin_pct=0.02)
        dimensions[os.path.basename(base_out)] = export_image(cropped, base_out, max_dim=1800)

import json
with open('scratch/processed_dimensions.json', 'w') as f:
    json.dump(dimensions, f, indent=2)

print("\nALL ASSETS PROCESSED SUCCESSFULLY!")
