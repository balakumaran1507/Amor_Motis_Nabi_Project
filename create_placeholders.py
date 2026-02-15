#!/usr/bin/env python3
"""
Create placeholder images for testing CTF Wrapped system
Generates simple colored squares for chibi placeholders and a basic card template
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create folders
os.makedirs("../chibis", exist_ok=True)

print("🎨 Creating placeholder chibi images...")

# Chibi placeholders (400x400 colored squares with emoji)
chibis = {
    "chibi_chaotic_lover.png": ("🌈", (138, 43, 226)),  # Purple
    "chibi_heartbreaker.png": ("💔", (220, 20, 60)),    # Crimson
    "chibi_player.png": ("🎮", (30, 144, 255)),         # Blue
    "chibi_overthinker.png": ("🤔", (255, 165, 0)),     # Orange
    "chibi_slow_burn.png": ("🔥", (255, 69, 0)),        # Red-orange
    "chibi_committed_one.png": ("🏔️", (50, 205, 50)),   # Green
    "chibi_hopeless_romantic.png": ("💘", (255, 105, 180))  # Pink
}

for filename, (emoji, color) in chibis.items():
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))  # Transparent
    draw = ImageDraw.Draw(img)

    # Draw colored circle
    draw.ellipse([50, 50, 350, 350], fill=color + (200,))  # Semi-transparent

    # Add emoji text (centered)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 150)
    except:
        font = ImageFont.load_default()

    # Center text
    bbox = draw.textbbox((0, 0), emoji, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (400 - text_width) // 2
    y = (400 - text_height) // 2 - 20  # Adjust for vertical centering

    draw.text((x, y), emoji, font=font, fill=(255, 255, 255, 255))

    img.save(f"../chibis/{filename}")
    print(f"  ✓ Created {filename}")

print("\n🎴 Creating card template background...")

# Card template (1080x1920)
card = Image.new('RGB', (1080, 1920), (10, 10, 10))  # Dark background
draw = ImageDraw.Draw(card)

# Add CYBERCOM branding at top
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 80)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
    stats_title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    stats_title_font = ImageFont.load_default()

# Top border line
draw.rectangle([0, 0, 1080, 5], fill=(255, 107, 53))  # Orange

# CYBERCOM text
draw.text((540, 80), "CYBERCOM", font=title_font, fill=(255, 255, 255), anchor="mm")
draw.text((540, 150), "CTF WRAPPED 2025", font=subtitle_font, fill=(255, 107, 53), anchor="mm")

# Archetype title area (will be added by script)
draw.text((540, 280), "[ARCHETYPE]", font=stats_title_font, fill=(200, 200, 200), anchor="mm")

# Center area for chibi (400x400 centered)
# chibi_x = (1080 - 400) // 2 = 340
# chibi_y = 600 (approx center)
# Draw placeholder box
draw.rectangle([340, 400, 740, 800], outline=(255, 107, 53), width=3)
draw.text((540, 600), "CHIBI HERE", font=subtitle_font, fill=(100, 100, 100), anchor="mm")

# Stats box at bottom
stats_box_y = 950
stats_box_height = 850

# Draw stats box background
draw.rectangle([50, stats_box_y, 1030, stats_box_y + stats_box_height],
               fill=(20, 20, 20), outline=(255, 107, 53), width=3)

# Stats title
draw.text((150, stats_box_y + 50), "► COMBAT STATISTICS", font=stats_title_font,
          fill=(255, 107, 53))

# Placeholder stat lines (will be filled by script)
stat_y = stats_box_y + 150
line_height = 80

placeholders = [
    "► SOLVED: 00/22",
    "► RANK: #000",
    "► TIME: 0h 0m",
    "► FAVORITE: Category"
]

for placeholder in placeholders:
    draw.text((150, stat_y), placeholder, font=subtitle_font, fill=(150, 150, 150))
    stat_y += line_height

# Bottom border
draw.rectangle([0, 1915, 1080, 1920], fill=(255, 107, 53))

# Valentine theme decorative elements
# Small hearts in corners
heart_positions = [(100, 200), (980, 200), (100, 1700), (980, 1700)]
for pos in heart_positions:
    draw.text(pos, "♥", font=stats_title_font, fill=(255, 107, 53, 100))

# Save card template
card.save("../card_bg.png")
print("  ✓ Created card_bg.png")

print("\n✅ ALL PLACEHOLDERS CREATED!")
print("\n📂 Files created:")
print("  • card_bg.png (1080x1920)")
print("  • chibis/ folder with 7 placeholder PNGs")
print("\n💡 You can now test the system with these placeholders!")
print("   When ready, replace them with your real chibi images.")
print("\nNEXT STEP: Run card generation test!")
print("  cd 'files (2)'")
print("  source ctf_venv/bin/activate")
print("  python personalize_cards_v2.py")
