#!/usr/bin/env python3
"""
CTF Wrapped HTML Generator - Professional Edition (No Emojis)
Generates personalized HTML pages for each player using built-in csv module
"""

import csv
import os
import shutil
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

# Input files
CSV_FILE = "player_data.csv"
HTML_TEMPLATE = "wrapped_template.html"
CARDS_FOLDER = "personalized_cards"

# Output
OUTPUT_FOLDER = "wrapped_pages"
BASE_URL = "https://cybercom-ctf-wrapped.netlify.app"

# ============================================
# ARCHETYPE DESCRIPTIONS
# ============================================

ARCHETYPE_DESCRIPTIONS = {
    "The Hopeless Romantic": "You approached every challenge with patience and dedication. Like someone who savors every moment of a mission, you solved puzzles methodically and enjoyed the journey. You value deep tactical connections and meaningful progress over quick wins.",
    "The Player": "Strategic and efficient, you cherry-picked challenges that gave you the best return on investment. You're the type who knows exactly what they want and goes for it without wasting time. In missions and in the field, you play to win smartly.",
    "The Committed One": "You never gave up, even on the hardest challenges. Your persistence and determination are unmatched. Like someone who fights for the cause, you kept pushing through obstacles until you succeeded. You believe in seeing things through to the end.",
    "The Heartbreaker": "You started strong with impressive early engagement, but then... you vanished. Like a high-profile asset that goes dark mid-operation, you left Act 2 behind. Your early impact was significant, but your mission remains incomplete.",
    "The Overthinker": "Every challenge required deep analysis. You considered every angle, used hints thoughtfully, and made sure you understood each step. You don't rush into solutions - you analyze the data completely before execution.",
    "The Chaotic Lover": "Your approach was beautifully unpredictable! You jumped between challenges, categories, and difficulty levels with wild abandon. You brought energetic chaos to your operative journey, finding success through sheer tactical spontaneity.",
    "The Slow Burn": "You started cautiously but built momentum as you went. Your improvement over time was impressive - each challenge made you stronger. You proved that steady growth and tactical patience lead to operational success."
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_badges_html(badges_str, archetype):
    """Generate HTML for badges section without emojis"""
    
    if not badges_str or badges_str.strip() == "":
        badges_list = [archetype]
    else:
        badges_list = [b.strip() for b in str(badges_str).split(',')]
        if archetype not in badges_list:
            badges_list.append(archetype)
    
    html = ""
    for badge in badges_list:
        # Using a sleek css-based badge instead of emoji
        badge_class = badge.lower().replace(" ", "-")
        html += f'<div class="badge-item badge-{badge_class}" title="{badge}">{badge}</div>\n                '
    
    return html

def generate_html_page(player_data, template_html, cards_folder, output_folder, base_url):
    """Generate personalized HTML page for one player"""
    
    username = str(player_data['Username'])
    archetype = str(player_data['Archetype'])
    solved = str(player_data['Total_Solved'])
    total = str(player_data.get('Total_Available', '22'))
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data.get('Fav_Category', 'Generalist'))
    
    description = ARCHETYPE_DESCRIPTIONS.get(archetype, "You have a unique approach to operative challenges!")
    
    card_filename = f"{username}_card.png"
    card_url = f"./cards/{card_filename}"
    
    # Copy card image to output folder
    card_src = os.path.join(cards_folder, card_filename)
    if os.path.exists(card_src):
        cards_output_dir = os.path.join(output_folder, "cards")
        os.makedirs(cards_output_dir, exist_ok=True)
        card_dest = os.path.join(cards_output_dir, card_filename)
        shutil.copy2(card_src, card_dest)
    else:
        # Try searching in wrapped_pages/cards if localized
        alt_card_src = os.path.join(output_folder, "cards", card_filename)
        if not os.path.exists(alt_card_src):
            print(f"  ⚠️  Warning: Card not found for {username}")
            card_url = ""
    
    badges_html = generate_badges_html(player_data.get('Badges', ''), archetype)
    page_url = f"{base_url}/{username}.html"
    
    html = template_html
    replacements = {
        '{{USERNAME}}': username,
        '{{ARCHETYPE}}': archetype,
        '{{ARCHETYPE_DESCRIPTION}}': description,
        '{{CARD_URL}}': card_url,
        '{{SOLVED}}': solved,
        '{{TOTAL}}': total,
        '{{RANK}}': rank,
        '{{TIME}}': time_display,
        '{{CATEGORY}}': category,
        '{{BADGES_HTML}}': badges_html,
        '{{PAGE_URL}}': page_url
    }
    
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    
    output_path = os.path.join(output_folder, f"{username}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path

def main():
    print("=" * 60)
    print("CTF WRAPPED HTML GENERATOR (PROFESSIONAL)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    try:
        with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            template_html = f.read()
        print("  ✓ Template loaded")
    except FileNotFoundError:
        print(f"  ❌ Error: Template file '{HTML_TEMPLATE}' not found!")
        return
    
    print(f"\n📊 Reading player data from {CSV_FILE}...")
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
    
    print(f"\n🎨 Generating personalized pages...")
    print("-" * 60)
    
    generated_count = 0
    for player_data in players:
        try:
            generate_html_page(
                player_data, 
                template_html, 
                CARDS_FOLDER, 
                OUTPUT_FOLDER,
                BASE_URL
            )
            generated_count += 1
            if generated_count % 20 == 0:
                print(f"  ...Generated {generated_count} pages")
        except Exception as e:
            print(f"  ❌ Error generating page for {player_data.get('Username', 'Unknown')}: {e}")
    
    print("-" * 60)
    print(f"\n✅ COMPLETE!")
    print(f"   Successfully generated: {generated_count} pages")
    
if __name__ == "__main__":
    main()
