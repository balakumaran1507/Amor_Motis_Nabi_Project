#!/usr/bin/env python3
"""
CTF Data Processor - Transform team-based CTF data to individual player data
Converts your CSV exports into player_data.csv format needed for Wrapped
"""

import pandas as pd
from collections import defaultdict

# ============================================
# CONFIGURATION
# ============================================

# Input files (adjust paths if needed)
USERS_CSV = "../users (1).csv"
SUBMISSIONS_CSV = "../submissions (1).csv"
SCOREBOARD_CSV = "../scoreboard (1).csv"

# Output file
OUTPUT_CSV = "../player_data.csv"

# ============================================
# ARCHETYPE LOGIC (Simplified for ASAP launch)
# ============================================

def calculate_archetype(stats):
    """
    Calculate player archetype based on their behavior

    Args:
        stats: Dictionary with player statistics

    Returns:
        Archetype name (str)
    """
    total_solved = stats['total_solved']
    total_available = stats['total_available']
    completion = stats['completion_percent']
    correct_submissions = stats['correct_submissions']
    incorrect_submissions = stats['incorrect_submissions']

    # Calculate attempts ratio
    if correct_submissions > 0:
        attempts_ratio = incorrect_submissions / correct_submissions
    else:
        attempts_ratio = 999  # Very high if never solved anything

    # Archetype classification (simplified version)
    if completion == 100:
        return "The Committed One"
    elif completion >= 80:
        return "The Hopeless Romantic"
    elif completion >= 50:
        return "The Slow Burn"
    elif total_solved >= 5 and attempts_ratio < 2:
        return "The Player"  # Strategic, few wrong attempts
    elif total_solved >= 3 and attempts_ratio > 5:
        return "The Overthinker"  # Many attempts per solve
    elif total_solved >= 1 and completion < 30:
        return "The Heartbreaker"  # Started but didn't finish
    else:
        return "The Chaotic Lover"  # Default

# ============================================
# MAIN PROCESSING
# ============================================

def main():
    print("=" * 70)
    print("CTF DATA PROCESSOR - Individual Player Wrapped Data Generator")
    print("=" * 70)

    # Read CSV files
    print("\n📂 Reading CSV files...")
    try:
        users_df = pd.read_csv(USERS_CSV)
        submissions_df = pd.read_csv(SUBMISSIONS_CSV)
        scoreboard_df = pd.read_csv(SCOREBOARD_CSV)
        print(f"  ✓ Users: {len(users_df)} rows")
        print(f"  ✓ Submissions: {len(submissions_df)} rows")
        print(f"  ✓ Scoreboard: {len(scoreboard_df)} rows")
    except Exception as e:
        print(f"  ❌ Error reading CSV files: {e}")
        return

    # Filter to only PLAYER role (exclude ADMIN, ORGANIZER)
    print("\n🎯 Filtering players...")
    players_df = users_df[users_df['Role'] == 'PLAYER'].copy()
    print(f"  ✓ Found {len(players_df)} players (excluding admins/organizers)")

    # Calculate total available challenges
    unique_challenges = submissions_df['Challenge'].unique()
    total_challenges = len(unique_challenges)
    print(f"\n📊 Total challenges in CTF: {total_challenges}")

    # Process each player
    print("\n🔄 Processing individual player statistics...")
    print("-" * 70)

    player_stats = []

    for _, player in players_df.iterrows():
        username = player['Username']
        email = player['Email']
        team = player['Team'] if pd.notna(player['Team']) else 'No Team'

        # Get this player's submissions
        player_submissions = submissions_df[submissions_df['Username'] == username]

        # Count correct and incorrect submissions
        correct = player_submissions[player_submissions['Correct'] == 'Yes']
        incorrect = player_submissions[player_submissions['Correct'] == 'No']

        total_solved = len(correct['Challenge'].unique())  # Unique challenges solved
        correct_submissions = len(correct)
        incorrect_submissions = len(incorrect)
        total_submissions = correct_submissions + incorrect_submissions

        # Calculate completion percentage
        completion_percent = (total_solved / total_challenges * 100) if total_challenges > 0 else 0

        # Calculate total points
        total_points = correct['Points Awarded'].sum()

        # Get time spent (calculate from first to last submission)
        if len(player_submissions) > 0:
            player_submissions['Timestamp'] = pd.to_datetime(player_submissions['Timestamp'])
            first_sub = player_submissions['Timestamp'].min()
            last_sub = player_submissions['Timestamp'].max()
            time_diff = last_sub - first_sub
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            time_display = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        else:
            time_display = "0m"

        # Get most attempted category (favorite category)
        if len(player_submissions) > 0:
            # Try to extract category from challenge name (rough approximation)
            # You might need to adjust this based on your challenge naming
            challenge_names = player_submissions['Challenge'].tolist()
            if len(challenge_names) > 0:
                fav_category = challenge_names[0]  # First challenge as placeholder
                # Better: parse actual categories if available
            else:
                fav_category = "General"
        else:
            fav_category = "None"

        # Get team rank (if team is in scoreboard)
        team_rank = None
        if team != 'No Team':
            team_score_row = scoreboard_df[scoreboard_df['Team'] == team]
            if len(team_score_row) > 0:
                team_rank = int(team_score_row.iloc[0]['Rank'])

        if team_rank is None:
            # If no team or team not ranked, use individual score-based rank
            # (This is a rough estimate - you might want to refine)
            rank_display = "N/A"
        else:
            rank_display = str(team_rank)

        # Calculate archetype
        stats_dict = {
            'total_solved': total_solved,
            'total_available': total_challenges,
            'completion_percent': completion_percent,
            'correct_submissions': correct_submissions,
            'incorrect_submissions': incorrect_submissions
        }
        archetype = calculate_archetype(stats_dict)

        # Determine badges (simplified)
        badges = []
        if completion_percent == 100:
            badges.append("perfect_score")
        if total_solved > 0 and time_diff.total_seconds() < 7200:  # Solved in under 2 hours
            badges.append("speed_demon")

        badges_str = ','.join(badges) if badges else ""

        # Store player data
        player_stats.append({
            'Username': username,
            'Email': email,
            'Archetype': archetype,
            'Total_Solved': total_solved,
            'Total_Available': total_challenges,
            'Rank': rank_display,
            'Time_Display': time_display,
            'Fav_Category': fav_category,
            'Badges': badges_str
        })

        print(f"  ✓ {username:20s} | {archetype:25s} | Solved: {total_solved}/{total_challenges}")

    print("-" * 70)

    # Create DataFrame and save
    print(f"\n💾 Saving player data...")
    output_df = pd.DataFrame(player_stats)
    output_df.to_csv(OUTPUT_CSV, index=False)
    print(f"  ✓ Saved to: {OUTPUT_CSV}")
    print(f"  ✓ Total players: {len(output_df)}")

    # Summary statistics
    print(f"\n📈 ARCHETYPE DISTRIBUTION:")
    archetype_counts = output_df['Archetype'].value_counts()
    for archetype, count in archetype_counts.items():
        print(f"  • {archetype:25s}: {count:3d} players")

    print("\n" + "=" * 70)
    print("✅ COMPLETE! player_data.csv is ready for card/HTML generation!")
    print("=" * 70)
    print("\nNEXT STEPS:")
    print("1. Open player_data.csv and verify data looks correct")
    print("2. Create your 7 chibi character PNGs")
    print("3. Create your card_bg.png template")
    print("4. Run: python personalize_cards_v2.py")
    print("5. Run: python generate_html_pages.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
