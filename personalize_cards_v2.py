#!/usr/bin/env python3
"""
CTF Card Personalizer v5 - MASTER PRECISION EDITION
Generates Spotify-style wrap cards with 100% pixel-perfect code-only design.
Fixes all alignment, spacing, and overlap issues.
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
DIM_WHITE = (150, 150, 150)
GRID_COLOR = (30, 30, 30)
BORDER_COLOR = (50, 50, 50)

# ============================================
# PRECISION TOOLS
# ============================================

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_technical_viz(draw, rect):
    """Draws a centered, balanced technical visualization"""
    rx, ry, rw, rh = rect
    draw.rectangle([rx, ry, rx+rw, ry+rh], outline=(40, 40, 40), width=1)
    
    # Header for viz
    draw.text((rx + 15, ry + 15), "BIOMETRIC_SIGNATURE", font=get_font(14), fill=DIM_WHITE)
    
    # Viz elements
    bar_margin = 40
    avail_w = rw - (bar_margin * 2)
    curr_y = ry + 60
    for i in range(7):
        # Background bar
        draw.rectangle([rx + bar_margin, curr_y, rx + bar_margin + avail_w, curr_y + 12], fill=(25, 25, 25))
        # Foreground bar (Data)
        data_w = random.randint(30, avail_w)
        draw.rectangle([rx + bar_margin, curr_y, rx + bar_margin + data_w, curr_y + 12], fill=ACCENT_COLOR)
        curr_y += 35

    # Corner Accents
    acc = 25
    # TL
    draw.line([(rx-5, ry-5), (rx+acc, ry-5)], fill=ACCENT_COLOR, width=2)
    draw.line([(rx-5, ry-5), (rx-5, ry+acc)], fill=ACCENT_COLOR, width=2)
    # BR
    draw.line([(rx+rw+5, ry+rh+5), (rx+rw+5-acc, ry+rh+5)], fill=ACCENT_COLOR, width=2)
    draw.line([(rx+rw+5, ry+rh+5), (rx+rw+5, ry+rh+5-acc)], fill=ACCENT_COLOR, width=2)

def personalize_card(player_data):
    username = str(player_data['Username']).upper()
    archetype = str(player_data['Archetype']).upper()
    solved = str(player_data['Total_Solved'])
    total = str(player_data.get('Total_Available', '22'))
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data.get('Fav_Category', 'Generalist')).upper()

    # 1. Base Canvas
    card = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(card)
    
    # 2. Tech Grid
    grid_step = 60
    for x in range(0, WIDTH, grid_step):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, grid_step):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

    # 3. Outer Frame
    margin = 45
    draw.rectangle([margin, margin, WIDTH-margin, HEIGHT-margin], outline=BORDER_COLOR, width=2)
    
    # 4. Header Labels
    label_font = get_font(18)
    draw.text((margin + 20, margin + 20), "INTEL_REPORT_V5.0", font=label_font, fill=DIM_WHITE)
    
    status_text = "ACCESS: ENCRYPTED"
    s_bbox = draw.textbbox((0, 0), status_text, font=label_font)
    draw.text((WIDTH - margin - 20 - (s_bbox[2]-s_bbox[0]), margin + 20), status_text, font=label_font, fill=ACCENT_COLOR)

    # 5. Operative Name Block
    name_font = get_font(105)
    n_bbox = draw.textbbox((0, 0), username, font=name_font)
    draw.text((CENTER_X - (n_bbox[2]-n_bbox[0])//2, 180), username, font=name_font, fill=WHITE)
    
    context_font = get_font(24)
    c_text = "CYBER_MISSION_RECAP // 2026"
    c_bbox = draw.textbbox((0, 0), c_text, font=context_font)
    draw.text((CENTER_X - (c_bbox[2]-c_bbox[0])//2, 305), c_text, font=context_font, fill=ACCENT_COLOR)

    # 6. Archetype Display
    arch_font = get_font(52)
    a_bbox = draw.textbbox((0, 0), archetype, font=arch_font)
    draw.text((CENTER_X - (a_bbox[2]-a_bbox[0])//2, 420), archetype, font=arch_font, fill=WHITE)

    # 7. Viz Section
    draw_technical_viz(draw, (180, 530, 440, 320))

    # 8. Precise Metric Table
    table_y = 940
    table_margin = 100
    row_height = 95
    
    section_font = get_font(22)
    draw.text((table_margin, table_y - 50), "► OPERATIONAL_METRICS", font=section_font, fill=ACCENT_COLOR)
    
    metrics = [
        ("TARGETS_RESOLVED", f"{solved} / {total}"),
        ("FIELD_PERCENTILE", f"RANK_{rank}"),
        ("MISSION_DURATION", time_display),
        ("CORE_SPECIALTY", category)
    ]
    
    label_f = get_font(20)
    value_f = get_font(42)
    
    curr_y = table_y
    for label, value in metrics:
        # Divider
        draw.line([(table_margin, curr_y + 85), (WIDTH - table_margin, curr_y + 85)], fill=(45, 45, 45), width=1)
        
        # Label (Left)
        draw.text((table_margin, curr_y), label, font=label_f, fill=DIM_WHITE)
        
        # Value (Right) - with scaling for long strings
        v_font = value_f
        if len(value) > 18:
            v_font = get_font(32)
        elif len(value) > 14:
            v_font = get_font(36)
            
        v_bbox = draw.textbbox((0, 0), value, font=v_font)
        draw.text((WIDTH - table_margin - (v_bbox[2]-v_bbox[0]), curr_y + 25), value, font=v_font, fill=WHITE)
        
        curr_y += row_height

    # 9. Master Footer
    footer_f = get_font(18)
    serial = f"SERIAL: {random.randint(100000, 999999)}-{random.randint(10, 99)}"
    draw.text((margin + 20, HEIGHT - margin - 45), serial, font=footer_f, fill=(60, 60, 60))
    
    tagline = "CYBER_COMMAND_PROPERTY_2026"
    t_bbox = draw.textbbox((0, 0), tagline, font=footer_f)
    draw.text((WIDTH - margin - 20 - (t_bbox[2]-t_bbox[0]), HEIGHT - margin - 45), tagline, font=footer_f, fill=(60, 60, 60))

    # Save
    output_path = os.path.join(OUTPUT_FOLDER, f"{player_data['Username']}_card.png")
    card.save(output_path, "PNG")
    return output_path

def main():
    print("=" * 60)
    print("CTF WRAPPED CARD GENERATOR - V5 MASTER PRECISION")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    players = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append(row)
    
    print(f"🚀 Generating {len(players)} pixel-perfect reports...")
    for i, player in enumerate(players):
        personalize_card(player)
        if (i+1) % 20 == 0: print(f"  ...Produced {i+1} cards")
            
    print("-" * 60)
    print(f"✅ FINALIZED: Optimization Complete.")

if __name__ == "__main__":
    main()
