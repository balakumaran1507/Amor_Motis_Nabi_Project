#!/usr/bin/env python3
"""
CTF Wrapped HTML Generator
Generates personalized HTML pages for each player
"""

import pandas as pd
import os
from pathlib import Path
import shutil

# ============================================
# CONFIGURATION
# ============================================

# Input files
CSV_FILE = "../player_data.csv"  # FULL DATASET - ALL 163 PLAYERS
HTML_TEMPLATE = "wrapped_template.html"
CARDS_FOLDER = "personalized_cards"  # Folder with generated cards

# Output
OUTPUT_FOLDER = "../wrapped_pages"  # Output to parent directory for easy Netlify upload
BASE_URL = "https://cybercom-ctf-wrapped.netlify.app"  # Will update after first deploy

# ============================================
# ARCHETYPE DESCRIPTIONS
# ============================================

ARCHETYPE_DESCRIPTIONS = {
    "The Hopeless Romantic": "You approached every challenge with patience and dedication. Like someone who savors every moment of a relationship, you solved puzzles methodically and enjoyed the journey. You value deep connections and meaningful progress over quick wins.",
    
    "The Player": "Strategic and efficient, you cherry-picked challenges that gave you the best return on investment. You're the type who knows exactly what they want and goes for it without wasting time. In CTFs and in life, you play to win smartly.",
    
    "The Committed One": "You never gave up, even on the hardest challenges. Your persistence and determination are unmatched. Like someone who fights for what they love, you kept pushing through obstacles until you succeeded. You believe in seeing things through to the end.",
    
    "The Heartbreaker": "You started strong with impressive early engagement, but then... you vanished. Like someone who ghosts after a few great dates, you left Act 2 behind. Maybe you got busy, maybe you moved on - either way, you left a mark before disappearing.",
    
    "The Overthinker": "Every challenge required deep analysis. You considered every angle, used hints thoughtfully, and made sure you understood each step. Like someone who analyzes every text message, you don't rush into solutions - you think them through completely.",
    
    "The Chaotic Lover": "Your approach was beautifully unpredictable! You jumped between challenges, categories, and difficulty levels with wild abandon. Like someone who thrives on spontaneity, you brought energetic chaos to your CTF journey. And honestly? It worked for you.",
    
    "The Slow Burn": "You started cautiously but built momentum as you went. Your improvement over time was impressive - each challenge made you stronger. Like a relationship that grows deeper with time, you proved that steady growth and patience lead to success."
}

# Badge emoji mapping
BADGE_EMOJIS = {
    "speed_demon": "⚡",
    "perfect_score": "💯",
    "The Hopeless Romantic": "💘",
    "The Player": "🎮",
    "The Committed One": "🏔️",
    "The Heartbreaker": "💔",
    "The Overthinker": "🤔",
    "The Chaotic Lover": "🌈",
    "The Slow Burn": "🔥"
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_badges_html(badges_str, archetype):
    """Generate HTML for badges section"""
    
    if pd.isna(badges_str) or badges_str == "":
        badges_list = [archetype]
    else:
        badges_list = [b.strip() for b in str(badges_str).split(',')]
        if archetype not in badges_list:
            badges_list.append(archetype)
    
    html = ""
    for badge in badges_list:
        emoji = BADGE_EMOJIS.get(badge, "🏅")
        html += f'<div class="badge" title="{badge}">{emoji}</div>\n                '
    
    return html

def generate_html_page(player_data, template_html, cards_folder, output_folder, base_url):
    """
    Generate personalized HTML page for one player
    
    Args:
        player_data: Dictionary with player info
        template_html: HTML template string
        cards_folder: Path to folder with card images
        output_folder: Path to save HTML pages
        base_url: Base URL where pages will be hosted
    
    Returns:
        Path to generated HTML file
    """
    
    # Extract player data
    username = str(player_data['Username'])
    archetype = str(player_data['Archetype'])
    solved = str(player_data['Total_Solved'])
    total = str(player_data['Total_Available'])
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data['Fav_Category'])
    
    # Get archetype description
    description = ARCHETYPE_DESCRIPTIONS.get(archetype, "You have a unique approach to CTF challenges!")
    
    # Card URL (will be uploaded with HTML)
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
        print(f"  ⚠️  Warning: Card not found for {username}")
        card_url = ""
    
    # Generate badges HTML
    badges_html = generate_badges_html(player_data.get('Badges', ''), archetype)
    
    # Page URL
    page_url = f"{base_url}/{username}.html"
    
    # Replace placeholders
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
    
    # Save HTML file
    output_path = os.path.join(output_folder, f"{username}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ Generated page for {username}")
    return output_path

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate all HTML pages"""
    
    print("=" * 60)
    print("CTF WRAPPED HTML GENERATOR")
    print("=" * 60)
    
    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Read template
    print(f"\n📄 Reading HTML template...")
    try:
        with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            template_html = f.read()
        print("  ✓ Template loaded")
    except FileNotFoundError:
        print(f"  ❌ Error: Template file '{HTML_TEMPLATE}' not found!")
        return
    
    # Read player data
    print(f"\n📊 Reading player data from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"  ✓ Found {len(df)} players")
    except FileNotFoundError:
        print(f"  ❌ Error: File '{CSV_FILE}' not found!")
        return
    
    # Check cards folder
    if not os.path.exists(CARDS_FOLDER):
        print(f"\n  ⚠️  Warning: Cards folder '{CARDS_FOLDER}' not found!")
        print("  Pages will be generated without card images.")
    
    # Generate pages
    print(f"\n🎨 Generating personalized pages...")
    print("-" * 60)
    
    generated_count = 0
    
    for index, row in df.iterrows():
        player_data = row.to_dict()
        
        try:
            generate_html_page(
                player_data, 
                template_html, 
                CARDS_FOLDER, 
                OUTPUT_FOLDER,
                BASE_URL
            )
            generated_count += 1
        except Exception as e:
            print(f"  ❌ Error generating page for {row['Username']}: {e}")
    
    print("-" * 60)
    print(f"\n✅ COMPLETE!")
    print(f"   Successfully generated: {generated_count} pages")
    print(f"\n📁 Pages saved to: {OUTPUT_FOLDER}/")
    print(f"   Card images in: {OUTPUT_FOLDER}/cards/")
    
    print(f"\n📤 NEXT STEPS:")
    print(f"   1. Go to https://app.netlify.com/drop")
    print(f"   2. Drag the '{OUTPUT_FOLDER}' folder onto the page")
    print(f"   3. Netlify will give you a URL (e.g., https://random-name.netlify.app)")
    print(f"   4. Update BASE_URL in this script with that URL")
    print(f"   5. Re-run the script to update share links")
    print(f"   6. Upload again to Netlify")
    print(f"   7. Done! Each player URL: https://your-site.netlify.app/username.html")
    
    print("=" * 60)

# ============================================
# RUN SCRIPT
# ============================================

if __name__ == "__main__":
    main()
