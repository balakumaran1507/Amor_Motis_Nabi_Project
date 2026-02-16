#!/usr/bin/env python3
"""
CTF Card Personalizer v4 - ZERO IMAGE EDITION
Generates Spotify-style wrap cards using 100% code. No background images, no chibis.
Technical, professional, premium data-driven aesthetic.
"""

import csv
import os
import random
from PIL import Image, ImageDraw, ImageFont

# ============================================
# CONFIGURATION
# ============================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_PATH, "player_data.csv")
OUTPUT_FOLDER = os.path.join(BASE_PATH, "personalized_cards")

# Dimensions (Spotify Card Aspect Ratio)
WIDTH, HEIGHT = 800, 1422 
CENTER_X = WIDTH // 2

# Font file (macOS system font)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Colors from Infra/Cybercom Theme
BG_COLOR = (5, 5, 5)        # Deep Black
ACCENT_COLOR = (255, 107, 53) # Cyber Orange
WHITE = (255, 255, 255)
DIM_WHITE = (140, 140, 140)
GRID_COLOR = (25, 25, 25)
BORDER_COLOR = (40, 40, 40)

# ============================================
# GENERATION LOGIC
# ============================================

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_grid(draw):
    step_size = 50
    for x in range(0, WIDTH, step_size):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, step_size):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

def draw_abstract_data(draw, x, y, width, height):
    """Draws a professional technical data-visualization looking element"""
    # Draw a technical frame
    draw.rectangle([x, y, x + width, y + height], outline=BORDER_COLOR, width=1)
    
    # Draw some 'fake' data bars
    curr_y = y + 40
    for _ in range(8):
        bar_w = random.randint(100, width - 100)
        draw.rectangle([x + 40, curr_y, x + 40 + bar_w, curr_y + 15], fill=(30, 30, 30))
        draw.rectangle([x + 40, curr_y, x + 40 + (bar_w // 2), curr_y + 15], fill=ACCENT_COLOR)
        curr_y += 35
    
    # Draw some technical corner accents
    acc = 20
    draw.line([(x, y), (x + acc, y)], fill=ACCENT_COLOR, width=3)
    draw.line([(x, y), (x, y + acc)], fill=ACCENT_COLOR, width=3)
    draw.line([(x + width, y + height), (x + width - acc, y + height)], fill=ACCENT_COLOR, width=3)
    draw.line([(x + width, y + height), (x + width, y + height - acc)], fill=ACCENT_COLOR, width=3)

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

    # 3. Framing & Branding
    margin = 50
    draw.rectangle([margin, margin, WIDTH-margin, HEIGHT-margin], outline=BORDER_COLOR, width=2)
    
    # Header Section
    header_f = get_font(18)
    draw.text((margin + 25, margin + 25), "OPERATIVE_INTEL_SYSTEM_V4.0", font=header_f, fill=DIM_WHITE)
    draw.text((WIDTH - margin - 230, margin + 25), "ACCESS_STATUS: ENCRYPTED", font=header_f, fill=ACCENT_COLOR)

    # 4. Main Operative Identifier
    name_font = get_font(90)
    bbox = draw.textbbox((0, 0), username, font=name_font)
    draw.text((CENTER_X - (bbox[2]-bbox[0])//2, 200), username, font=name_font, fill=WHITE)
    
    sub_font = get_font(26)
    draw.text((CENTER_X - 120, 310), "CTF RECAP // 2026", font=sub_font, fill=ACCENT_COLOR)

    # 5. Archetype Analysis Section
    arch_title_font = get_font(48)
    bbox = draw.textbbox((0, 0), archetype, font=arch_title_font)
    draw.text((CENTER_X - (bbox[2]-bbox[0])//2, 420), archetype, font=arch_title_font, fill=WHITE)
    
    # Center decorative element (Replacing Chibi)
    draw_abstract_data(draw, 150, 520, 500, 350)

    # 6. Performance Metrics Section
    stats_y = 950
    box_margin = 100
    
    # Section Header
    draw.text((box_margin, stats_y - 60), "► FIELD_PERFORMANCE_METRICS", font=get_font(24), fill=ACCENT_COLOR)
    
    metrics_font = get_font(42)
    label_font = get_font(20)
    curr_y = stats_y
    
    metrics = [
        ("TARGETS_RESOLVED", f"{solved} / {total}"),
        ("MISSION_PERCENTILE", f"RANK_{rank}"),
        ("ACTIVE_OP_TIME", time_display),
        ("CORE_SPECIALIZATION", category.upper())
    ]

    for label, value in metrics:
        # Draw dotted line divider
        draw.line([(box_margin, curr_y + 85), (WIDTH - box_margin, curr_y + 85)], fill=(40, 40, 40), width=1)
        
        draw.text((box_margin, curr_y), label, font=label_font, fill=DIM_WHITE)
        # Value aligned to right
        v_bbox = draw.textbbox((0, 0), value, font=metrics_font)
        draw.text((WIDTH - box_margin - (v_bbox[2]-v_bbox[0]), curr_y + 25), value, font=metrics_font, fill=WHITE)
        
        curr_y += 110

    # 7. Bottom Verification Code
    footer_f = get_font(18)
    auth_code = f"AUTH-HEX-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    draw.text((margin + 25, HEIGHT - margin - 40), auth_code, font=footer_f, fill=(50, 50, 50))
    draw.text((WIDTH - margin - 220, HEIGHT - margin - 40), "CYBERCOM_INTEL_REPORT", font=footer_f, fill=(50, 50, 50))

    # Save
    output_path = os.path.join(OUTPUT_FOLDER, f"{player_data['Username']}_card.png")
    card.save(output_path, "PNG")
    return output_path

def main():
    print("=" * 60)
    print("CTF WRAPPED CARD GENERATOR - V4 ZERO IMAGE EDITION")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    players = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append(row)
    except FileNotFoundError:
        print(f"❌ Error: {CSV_FILE} not found")
        return
    
    print(f"🚀 Generating {len(players)} images via code only...")
    for i, player in enumerate(players):
        personalize_card(player)
        if (i+1) % 20 == 0:
            print(f"  ...Generated {i+1} records")
            
    print("-" * 60)
    print(f"✅ FINALIZED: 166 Encrypted Operative Reports Delivered.")

if __name__ == "__main__":
    main()
