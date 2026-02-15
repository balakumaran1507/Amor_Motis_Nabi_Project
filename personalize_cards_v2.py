#!/usr/bin/env python3
"""
CTF Card Personalizer v2 - Template Based
Uses blank template + overlays chibi + adds text
"""

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

# ============================================
# CONFIGURATION
# ============================================

# Input files
CSV_FILE = "../player_data.csv"  # FULL DATASET - ALL 163 PLAYERS
TEMPLATE_BG = "../card_bg.png"  # Your blank template (in parent dir)
CHIBI_FOLDER = "../chibis"  # Folder with 7 transparent chibi PNGs (in parent dir)

# Output folder
OUTPUT_FOLDER = "personalized_cards"

# Font file (macOS system font)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"  # macOS default

# ============================================
# CHIBI MAPPING
# ============================================

# Map archetype names to chibi filenames
CHIBI_MAP = {
    "The Hopeless Romantic": "chibi_hopeless_romantic.png",
    "The Player": "chibi_player.png",
    "The Committed One": "chibi_committed_one.png",
    "The Heartbreaker": "chibi_heartbreaker.png",
    "The Overthinker": "chibi_overthinker.png",
    "The Chaotic Lover": "chibi_chaotic_lover.png",
    "The Slow Burn": "chibi_slow_burn.png"
}

# ============================================
# TEXT POSITIONS (Adjust these to match your template)
# ============================================

# Archetype title position (centered, upper third)
TITLE_POSITION = (540, 280)  # X, Y - centered horizontally
TITLE_FONT_SIZE = 68
TITLE_COLOR = (255, 255, 255)  # White

# Chibi character position (centered, middle)
CHIBI_POSITION = (540, 600)  # X, Y - centered
CHIBI_SIZE = (400, 400)  # Width, Height

# Stats text positions (inside the stats box)
# Your template has stats box at bottom, adjust Y values to match
STATS_START_Y = 950  # Where first stat line starts
STATS_LINE_HEIGHT = 60  # Space between each stat line
STATS_X = 150  # Left margin inside stats box
STATS_FONT_SIZE = 40
STATS_COLOR = (255, 255, 255)  # White

# ============================================
# HELPER FUNCTIONS
# ============================================

def add_text_centered(draw, text, position, font, color):
    """Add centered text at position"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = position[0] - text_width // 2
    y = position[1] - text_height // 2
    draw.text((x, y), text, font=font, fill=color)

def add_text_left(draw, text, position, font, color):
    """Add left-aligned text at position"""
    draw.text(position, text, font=font, fill=color)

def personalize_card(player_data, template_path, chibi_folder, output_folder):
    """
    Generate personalized card for one player
    
    Args:
        player_data: Dictionary with player info
        template_path: Path to blank template image
        chibi_folder: Folder containing chibi PNGs
        output_folder: Where to save final card
    
    Returns:
        Path to generated card or None if error
    """
    
    # Get player info
    username = str(player_data['Username'])
    archetype = str(player_data['Archetype'])
    solved = str(player_data['Total_Solved'])
    total = str(player_data['Total_Available'])
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data['Fav_Category'])
    
    # Load template
    try:
        card = Image.open(template_path).convert('RGBA')
    except FileNotFoundError:
        print(f"  ❌ Template not found: {template_path}")
        return None
    
    # Load and paste chibi character
    chibi_filename = CHIBI_MAP.get(archetype)
    if chibi_filename:
        chibi_path = os.path.join(chibi_folder, chibi_filename)
        try:
            chibi = Image.open(chibi_path).convert('RGBA')
            
            # Resize chibi to fit
            chibi = chibi.resize(CHIBI_SIZE, Image.Resampling.LANCZOS)
            
            # Calculate position to center chibi
            chibi_x = CHIBI_POSITION[0] - CHIBI_SIZE[0] // 2
            chibi_y = CHIBI_POSITION[1] - CHIBI_SIZE[1] // 2
            
            # Paste chibi onto card (with transparency)
            card.paste(chibi, (chibi_x, chibi_y), chibi)
            
        except FileNotFoundError:
            print(f"  ⚠️  Chibi not found: {chibi_path}")
    else:
        print(f"  ⚠️  No chibi mapping for archetype: {archetype}")
    
    # Create drawing context
    draw = ImageDraw.Draw(card)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
        stats_font = ImageFont.truetype(FONT_PATH, STATS_FONT_SIZE)
    except:
        print("  ⚠️  Font not found, using default")
        title_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
    
    # Add archetype title (centered)
    add_text_centered(draw, archetype.upper(), TITLE_POSITION, title_font, TITLE_COLOR)
    
    # Add stats (left-aligned in stats box)
    stats_y = STATS_START_Y
    
    # Skip "COMBAT STATISTICS" header - already in template
    stats_y += STATS_LINE_HEIGHT + 20  # Move down past header
    
    # Add each stat line
    add_text_left(draw, f"► SOLVED: {solved}/{total}", 
                  (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► RANK: #{rank}", 
                  (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► TIME: {time_display}", 
                  (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► FAVORITE: {category}", 
                  (STATS_X, stats_y), stats_font, STATS_COLOR)
    
    # Convert back to RGB for saving as PNG
    card = card.convert('RGB')
    
    # Save personalized card
    output_path = os.path.join(output_folder, f"{username}_card.png")
    card.save(output_path, "PNG")
    
    print(f"  ✓ Generated card for {username} ({archetype})")
    return output_path

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate all cards"""
    
    print("=" * 60)
    print("CTF CARD PERSONALIZER V2 - TEMPLATE BASED")
    print("=" * 60)
    
    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Check template exists
    if not os.path.exists(TEMPLATE_BG):
        print(f"\n❌ ERROR: Template not found: {TEMPLATE_BG}")
        print("Please place your card_bg.png in this folder.")
        return
    
    # Check chibi folder exists
    if not os.path.exists(CHIBI_FOLDER):
        print(f"\n❌ ERROR: Chibi folder not found: {CHIBI_FOLDER}")
        print("Please create a 'chibis/' folder with your 7 chibi PNGs.")
        return
    
    # Read player data
    print(f"\n📊 Reading player data from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"  ✓ Found {len(df)} players")
    except FileNotFoundError:
        print(f"  ❌ Error: File '{CSV_FILE}' not found!")
        return
    
    # Generate cards
    print(f"\n🎨 Generating personalized cards...")
    print("-" * 60)
    
    generated_count = 0
    failed_count = 0
    
    for index, row in df.iterrows():
        player_data = row.to_dict()
        
        result = personalize_card(
            player_data,
            TEMPLATE_BG,
            CHIBI_FOLDER,
            OUTPUT_FOLDER
        )
        
        if result:
            generated_count += 1
        else:
            failed_count += 1
    
    # Summary
    print("-" * 60)
    print(f"\n✅ COMPLETE!")
    print(f"   Successfully generated: {generated_count} cards")
    if failed_count > 0:
        print(f"   Failed: {failed_count} cards")
    print(f"\n📁 Cards saved to: {OUTPUT_FOLDER}/")
    print("=" * 60)

# ============================================
# RUN SCRIPT
# ============================================

if __name__ == "__main__":
    main()
