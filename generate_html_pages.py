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
    "The Hopeless Romantic": "You treated every challenge like it mattered. While others were speedrunning for points, you actually read the descriptions, appreciated the theme, took your time. You didn't just solve challenges - you experienced them. Sure, you might not have the fastest time or the highest rank, but you finished what you started. You showed up consistently, tackled the hard stuff, and didn't give up when things got frustrating. That's rare. In a world of players chasing leaderboards, you remembered why this is supposed to be fun. You're the type who actually enjoys the journey, not just the destination. And honestly? That's the kind of energy that makes communities great. Keep doing your thing. 💘",
    "The Player": "You saw the scoreboard and said \"bet.\" You didn't waste time on challenges that didn't matter - you cherry-picked the high-value targets and demolished them. Strategic. Efficient. Ruthless. While everyone else was grinding through every challenge like it's homework, you optimized for points-per-hour. You knew exactly what you wanted and went straight for it. No emotional attachment, just pure calculation. Some people might call that lazy. But you call it smart. Why spend 3 hours on a 100-point challenge when you can grab five 200-pointers in the same time? You played the game within the game. And honestly? Respect. You know your worth and you don't waste time proving it to anyone. 🎮",
    "The Committed One": "100%. Perfect score. Every. Single. Challenge. While others were sleeping, you were solving. While others gave up on the hard ones, you dug deeper. You didn't just participate - you conquered. That kind of dedication doesn't come from nowhere. Let's be honest: you probably spent more hours on this CTF than anyone else. You probably hit walls that made you want to quit. But you didn't. Because for you, \"good enough\" isn't in the vocabulary. Some people play CTFs for fun. You play to win. And the scary part? You actually pull it off. Whatever you're chasing - validation, mastery, or just the high of completion - you got it. Well done. Now go touch some grass. 🏔️",
    "The Heartbreaker": "You started this CTF like you had something to prove - and honestly? You proved it. Those early solves weren't luck. You had skills, strategy, and the kind of confidence that made other players nervous. Then you just... disappeared. No explanation, no goodbye. Classic ghost move. Here's the thing: you've got talent. That's obvious. What you don't have is the follow-through. Raw skill without commitment is just wasted potential. And potential doesn't win CTFs - persistence does. So next time, when it gets hard and you feel like bouncing... don't. Stick around. See what happens when you actually finish what you started. Your move. 💔",
    "The Overthinker": "You approached every challenge like it was a trap. Read the description five times. Checked for edge cases. Questioned everything. Probably asked for hints not because you couldn't solve it, but because you needed confirmation you were thinking about it right. And you know what? That's not wrong. Being thorough beats being fast when accuracy matters. But sometimes... sometimes you just gotta trust your gut and submit the flag. Analysis paralysis is real, and you know it. You've probably solved challenges in your head but second-guessed yourself out of the answer. The gap between knowing and doing? That's where you live. But here's the thing: all that overthinking means you actually understand what you're doing. You're not just guessing. You're learning. And that matters more than speed. Just... maybe trust yourself a little more next time? 🤔",
    "The Chaotic Lover": "Your solve order makes absolutely no sense. Easy challenge? Nah. Hard challenge? Sure, why not. Medium one you skipped? Forgot it existed. Your dashboard looked like a tornado hit it. But somehow... it worked? You bounced between categories like you were playing CTF bingo. No strategy, no plan, just pure vibes and energy. And honestly, watching your progress was either inspiring or anxiety-inducing, depending on who you ask. Some people need structure. You need chaos. Some people follow the path. You make your own and hope it leads somewhere interesting. The fact that you still solved a decent amount despite having zero organization is either impressive or concerning. Maybe both. Never change. The CTF scene needs more chaos agents like you. 🌈",
    "The Slow Burn": "You started slow. Like, really slow. First few challenges took you forever, and honestly, it looked rough. But then something clicked. Maybe you figured out the pattern. Maybe you learned a new technique. Maybe you just got mad enough to push through. Whatever it was, you started picking up speed. Each solve came faster than the last. You finished strong. That's growth in real-time. That's what learning looks like. While others plateaued, you kept improving. Your graph wasn't a spike - it was a curve, steadily climbing. You proved something important: starting slow doesn't mean finishing slow. Momentum builds. Skills compound. And sometimes the best way to win is to just keep showing up until you figure it out. You didn't give up when it was hard. And that's everything. 🔥"
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
