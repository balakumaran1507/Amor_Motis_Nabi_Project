#!/usr/bin/env python3
"""
CTF Card Personalizer v3 - Pure Code Edition
Generates Spotify-style wrap cards entirely using code (no background images).
Technical, professional, premium aesthetic.
"""

import csv
import os
from PIL import Image, ImageDraw, ImageFont

# ============================================
# CONFIGURATION
# ============================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_PATH, "player_data.csv")
CHIBI_FOLDER = os.path.join(BASE_PATH, "chibis")
OUTPUT_FOLDER = os.path.join(BASE_PATH, "personalized_cards")

# Dimensions (Spotify Card Aspect Ratio)
WIDTH, HEIGHT = 800, 1422 
CENTER_X = WIDTH // 2

# Font file (macOS system font)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    # Fallback for linux/other
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Colors from Infra/Cybercom Theme
BG_COLOR = (5, 5, 5)        # Deep Black
ACCENT_COLOR = (255, 107, 53) # Cyber Orange
WHITE = (255, 255, 255)
DIM_WHITE = (160, 160, 160)
GRID_COLOR = (30, 30, 30)

# ============================================
# CHIBI MAPPING
# ============================================

CHIBI_MAP = {
    "The Hopeless Romantic": "chibi_hopeless_romantic.png",
    "The Player": "chibi_player.png",
    "The Committed One": "chibi_commited _one.png",
    "The Heartbreaker": "chibi_heartbreaker.png",
    "The Overthinker": "chibi_overthinker.png",
    "The Chaotic Lover": "chibi_chaoticlover.png",
    "The Slow Burn": "chibi_slowburn.png"
}

# ============================================
# GENERATION LOGIC
# ============================================

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_grid(draw):
    step_size = 60
    for x in range(0, WIDTH, step_size):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, step_size):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

def personalize_card(player_data):
    username = str(player_data['Username']).upper()
    archetype = str(player_data['Archetype']).upper()
    solved = str(player_data['Total_Solved'])
    total = str(player_data.get('Total_Available', '22'))
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data.get('Fav_Category', 'Generalist'))

    # 1. Create Base Canvas
    card = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(card)
    
    # 2. Draw Technical Grid
    draw_grid(draw)

    # 3. Framing & Borders
    margin = 40
    draw.rectangle([margin, margin, WIDTH-margin, HEIGHT-margin], outline=(50, 50, 50), width=2)
    
    # Header Section
    draw.text((margin + 20, margin + 20), "SYSTEM_CARD_V3.0", font=get_font(18), fill=DIM_WHITE)
    draw.text((WIDTH - margin - 220, margin + 20), "STATUS: CLASSIFIED", font=get_font(18), fill=ACCENT_COLOR)

    # 4. Main Title (Operative Name)
    title_font = get_font(80)
    bbox = draw.textbbox((0, 0), username, font=title_font)
    draw.text((CENTER_X - (bbox[2]-bbox[0])//2, 180), username, font=title_font, fill=WHITE)
    
    # Sub-branding
    sub_font = get_font(24)
    draw.text((CENTER_X - 100, 280), "CTF WRAPPED // 2026", font=sub_font, fill=ACCENT_COLOR)

    # 5. Archetype Shield
    arch_font = get_font(42)
    bbox = draw.textbbox((0, 0), archetype, font=arch_font)
    # Background for archetype tag
    tag_width = bbox[2] - bbox[0] + 60
    draw.rectangle([CENTER_X - tag_width//2, 360, CENTER_X + tag_width//2, 430], fill=(20, 20, 20), outline=ACCENT_COLOR, width=1)
    draw.text((CENTER_X - (bbox[2]-bbox[0])//2, 375), archetype, font=arch_font, fill=WHITE)

    # 6. Chibi Character Placement
    chibi_filename = CHIBI_MAP.get(player_data['Archetype'])
    if chibi_filename:
        chibi_path = os.path.join(CHIBI_FOLDER, chibi_filename)
        if os.path.exists(chibi_path):
            chibi = Image.open(chibi_path).convert('RGBA')
            chibi = chibi.resize((480, 480), Image.Resampling.LANCZOS)
            card.paste(chibi, (CENTER_X - 240, 480), chibi)

    # 7. Mission Analytics Box
    stats_y = 1000
    box_margin = 80
    draw.rectangle([box_margin, stats_y - 20, WIDTH-box_margin, HEIGHT-140], outline=(80, 80, 80), width=1)
    
    # Header
    draw.text((box_margin + 30, stats_y), "► MISSION STATISTICS", font=get_font(28), fill=ACCENT_COLOR)
    
    stats_font = get_font(38)
    curr_y = stats_y + 80
    
    stats = [
        ("TARGETS NEUTRALIZED", f"{solved} / {total}"),
        ("FIELD RANKING", f"RANK_{rank}"),
        ("MISSION DURATION", time_display),
        ("TACTICAL SPECIALTY", category)
    ]

    for label, value in stats:
        draw.text((box_margin + 30, curr_y), label, font=get_font(22), fill=DIM_WHITE)
        draw.text((box_margin + 30, curr_y + 35), f"► {value}", font=stats_font, fill=WHITE)
        curr_y += 100

    # 8. Footer Branding
    footer_font = get_font(20)
    draw.text((CENTER_X - 180, HEIGHT - 80), "#CYBERCOMValentineCTF // 2026", font=footer_font, fill=(60, 60, 60))

    # Save
    output_path = os.path.join(OUTPUT_FOLDER, f"{player_data['Username']}_card.png")
    card.save(output_path, "PNG")
    return output_path

def main():
    print("=" * 60)
    print("CTF WRAPPED CARD GENERATOR - CODE ONLY EDITION")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    players = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append(row)
    
    print(f"🚀 Generating {len(players)} professional cards...")
    for i, player in enumerate(players):
        personalize_card(player)
        if (i+1) % 20 == 0:
            print(f"  ...Generated {i+1} cards")
            
    print("-" * 60)
    print(f"✅ SUCCESS: All {len(players)} cards generated without image dependencies.")

if __name__ == "__main__":
    main()
