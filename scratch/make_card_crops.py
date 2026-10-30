from PIL import Image

# 1. Smeltende sieraden
# Hand is at y=450..3150, x=200..2050 in 2252x3533
im_sieraden = Image.open('images/smeltende_sieraden03.png').convert('RGB')
# For 4:3: if height is 2400 (y=400..2800), width should be 3200 (need padding) OR width=2252, height=1689
# The hand is taller than wide, so let's crop around hand: y=400..2900 (h=2500).
# In 4:3 ratio: width = 2500 * 4 / 3 = 3333 -> we can pad with the wall color (230, 230, 230) and floor white
# OR crop around the key subject (the golden ring and hand): y=400..2000 (h=1600), w = 1600*4/3 = 2133 (fits inside 2252!)
card_sieraden = im_sieraden.crop((60, 420, 2193, 2020)) # 2133 x 1600 (4:3)
card_sieraden = card_sieraden.resize((1200, 900), Image.Resampling.LANCZOS)
card_sieraden.save('scratch/test_card_sieraden_4x3.jpg')

# 2. Stop poster
# Stop poster is 1800x2520. Subject (yellow stop light + man) is in center/upper part
im_stop = Image.open('images/projecten/stop/stop-poster-definitief.webp').convert('RGB')
# 4:3 crop centered on the figure and typography: w=1800, h=1350
# y=200..1550 captures the headline, yellow stop light, and bending man!
card_stop = im_stop.crop((0, 200, 1800, 1550)) # 1800 x 1350 (4:3)
card_stop = card_stop.resize((1200, 900), Image.Resampling.LANCZOS)
card_stop.save('scratch/test_card_stop_4x3.jpg')

# 3. Your Bubble (Can_03)
# 4:3 crop from Can_03
im_can = Image.open('images/Can_03.png').convert('RGB')
card_can = im_can.crop((1100, 250, 4700, 2950)) # 3600 x 2700 (4:3)
card_can = card_can.resize((1200, 900), Image.Resampling.LANCZOS)
card_can.save('scratch/test_card_can_4x3.jpg')

# 4. Whiplash
# 1920x1080. For 4:3: height=1080, width=1440
im_whip = Image.open('video/whiplash_poster.webp').convert('RGB')
card_whip = im_whip.crop((240, 0, 1680, 1080)) # 1440 x 1080 (4:3)
card_whip = card_whip.resize((1200, 900), Image.Resampling.LANCZOS)
card_whip.save('scratch/test_card_whip_4x3.jpg')

print("Card crops generated successfully!")
