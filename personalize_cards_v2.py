#!/usr/bin/env python3
"""
CTF Card Personalizer v2 - Professional Edition
Optimized for 768x1360 Template. No emojis. Professional typography.
"""

import csv
import os
from PIL import Image, ImageDraw, ImageFont

# ============================================
# CONFIGURATION
# ============================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_PATH, "player_data.csv")
TEMPLATE_BG = os.path.join(BASE_PATH, "chibis", "card bg.png")
CHIBI_FOLDER = os.path.join(BASE_PATH, "chibis")
OUTPUT_FOLDER = os.path.join(BASE_PATH, "personalized_cards")

# Font file (macOS system font - using bold where needed)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

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
# TEXT POSITIONS (Professional Scaling)
# ============================================

WIDTH, HEIGHT = 768, 1360
CENTER_X = WIDTH // 2

TITLE_POSITION = (CENTER_X, 235) 
TITLE_FONT_SIZE = 58  # Increased for professional presence

CHIBI_POSITION = (CENTER_X, 580) 
CHIBI_SIZE = (460, 460)

STATS_START_Y = 970 
STATS_LINE_HEIGHT = 70
STATS_X = 145
STATS_FONT_SIZE = 36  # Slightly larger for readability

# Colors from Infra theme
BG_COLOR = (12, 12, 12) # Dark theme background
ACCENT_COLOR = (255, 107, 53) # Cyber Orange
WHITE = (255, 255, 255)
DIM_WHITE = (200, 200, 200)

# ============================================
# HELPER FUNCTIONS
# ============================================

def add_text_centered(draw, text, position, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = position[0] - text_width // 2
    y = position[1] - text_height // 2
    draw.text((x, y), text, font=font, fill=color)

def add_text_left(draw, text, position, font, color):
    draw.text(position, text, font=font, fill=color)

def personalize_card(player_data, template_path, chibi_folder, output_folder):
    username = str(player_data['Username'])
    archetype = str(player_data['Archetype'])
    solved = str(player_data['Total_Solved'])
    total = str(player_data.get('Total_Available', '22'))
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data.get('Fav_Category', 'Generalist'))
    
    try:
        card = Image.open(template_path).convert('RGBA')
    except FileNotFoundError:
        print(f"  ❌ Template not found: {template_path}")
        return None
    
    # Ensure card is 768x1360
    if card.size != (WIDTH, HEIGHT):
        card = card.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(card)

    # 1. Clear placeholders with professional precision
    # Clear "2025" region (Top Right)
    draw.rectangle([380, 80, 750, 140], fill=BG_COLOR)
    # Archetype area
    draw.rectangle([80, 150, 680, 290], fill=BG_COLOR)
    # Chibi area
    draw.rectangle([220, 360, 580, 790], fill=BG_COLOR)
    # Stats area
    draw.rectangle([130, 840, 650, 1320], fill=BG_COLOR)

    # 2. Add technical "2026" text (Top Right)
    try:
        small_mono = ImageFont.truetype(FONT_PATH, 22)
    except:
        small_mono = ImageFont.load_default()
    add_text_left(draw, "CTF WRAPPED 2026", (485, 98), small_mono, ACCENT_COLOR)

    # 3. Paste chibi character
    chibi_filename = CHIBI_MAP.get(archetype)
    if chibi_filename:
        chibi_path = os.path.join(chibi_folder, chibi_filename)
        if os.path.exists(chibi_path):
            chibi = Image.open(chibi_path).convert('RGBA')
            chibi = chibi.resize(CHIBI_SIZE, Image.Resampling.LANCZOS)
            chibi_x = CHIBI_POSITION[0] - CHIBI_SIZE[0] // 2
            chibi_y = CHIBI_POSITION[1] - CHIBI_SIZE[1] // 2
            card.paste(chibi, (chibi_x, chibi_y), chibi)
        else:
            print(f"  ⚠️  Chibi not found: {chibi_path}")
    
    # 4. Add professional typography
    try:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
        stats_font = ImageFont.truetype(FONT_PATH, STATS_FONT_SIZE)
        header_font = ImageFont.truetype(FONT_PATH, 34)
    except:
        title_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
    
    # Archetype Title (Centered)
    add_text_centered(draw, archetype.upper(), TITLE_POSITION, title_font, WHITE)
    
    # Redraw "COMBAT STATISTICS" header
    add_text_left(draw, "► COMBAT STATISTICS", (STATS_X - 10, STATS_START_Y - 80), header_font, ACCENT_COLOR)

    stats_y = STATS_START_Y
    # Solved
    add_text_left(draw, "► SOLVED:", (STATS_X, stats_y), stats_font, DIM_WHITE)
    add_text_left(draw, f"{solved}/{total}", (STATS_X + 180, stats_y), stats_font, WHITE)
    
    stats_y += STATS_LINE_HEIGHT
    # Rank
    add_text_left(draw, "► RANK:", (STATS_X, stats_y), stats_font, DIM_WHITE)
    add_text_left(draw, f"#{rank}", (STATS_X + 180, stats_y), stats_font, WHITE)
    
    stats_y += STATS_LINE_HEIGHT
    # Time
    add_text_left(draw, "► TIME:", (STATS_X, stats_y), stats_font, DIM_WHITE)
    add_text_left(draw, f"{time_display}", (STATS_X + 180, stats_y), stats_font, WHITE)
    
    stats_y += STATS_LINE_HEIGHT
    # Favorite
    add_text_left(draw, "► CATEGORY:", (STATS_X, stats_y), stats_font, DIM_WHITE)
    add_text_left(draw, f"{category}", (STATS_X + 240, stats_y), stats_font, WHITE)
    
    card = card.convert('RGB')
    output_path = os.path.join(output_folder, f"{username}_card.png")
    card.save(output_path, "PNG")
    
    return output_path

def main():
    print("=" * 60)
    print("CTF CARD PERSONALIZER V2 (PROFESSIONAL EDITION)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    if not os.path.exists(TEMPLATE_BG):
        print(f"\n❌ ERROR: Template not found: {TEMPLATE_BG}")
        return
    
    players = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append(row)
        print(f"  ✓ Found {len(players)} players")
    except FileNotFoundError:
        print(f"  ❌ Error: File '{CSV_FILE}' not found!")
        return
    
    generated_count = 0
    for player_data in players:
        result = personalize_card(player_data, TEMPLATE_BG, CHIBI_FOLDER, OUTPUT_FOLDER)
        if result:
            generated_count += 1
            if generated_count % 20 == 0:
                print(f"  ...Generated {generated_count} cards")
    
    print("-" * 60)
    print(f"\n✅ COMPLETE! Generated {generated_count} cards")

if __name__ == "__main__":
    main()
