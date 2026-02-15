# CTF WRAPPED - COMPLETE TECHNICAL DOCUMENTATION
## Post-Event Personalized Results System

**Project:** Valentine's Day CTF 2025 - Wrapped Experience  
**Deadline:** Feb 17, 2026 10:00 AM Launch  
**Players:** ~90-100  
**Tech Stack:** Python, Google Sheets, Netlify, HTML/CSS, Google Apps Script  

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Data Flow](#3-data-flow)
4. [Components Breakdown](#4-components-breakdown)
5. [File Structure](#5-file-structure)
6. [Implementation Steps](#6-implementation-steps)
7. [Code & Scripts](#7-code--scripts)
8. [Testing & Validation](#8-testing--validation)
9. [Deployment](#9-deployment)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. PROJECT OVERVIEW

### **What We're Building**

A **"Spotify Wrapped"** style post-CTF experience where each player receives:
- Personalized archetype classification (7 types based on behavior)
- Custom-designed card with their stats
- Unique web page showing their results
- Email with link to their personal page
- Social sharing functionality

### **User Journey**

```
Player completes CTF (Feb 14-15)
          ↓
System collects data automatically
          ↓
Feb 15 (8 PM): CTF ends, data exported
          ↓
Feb 15 (9-11 PM): We process data & generate content
          ↓
Feb 17 (10 AM): Emails sent to all players
          ↓
Player clicks link → sees personalized web page
          ↓
Player shares on social media
          ↓
Viral marketing + community engagement! 🎉
```

### **Business Goals**

- **Engagement:** Keep players excited post-CTF
- **Marketing:** Social media sharing = organic reach
- **Retention:** Players want to come back for next CTF
- **Branding:** Professional, memorable experience
- **Data:** Collect feedback via form

---

## 2. SYSTEM ARCHITECTURE

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                     CTF PLATFORM                            │
│  (Custom Infrastructure - Collecting Data During Event)     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ CSV Exports (users, submissions, scoreboard)
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                   GOOGLE SHEETS                             │
│  - Data Import & Validation                                 │
│  - Archetype Calculation (Formulas)                         │
│  - Player Stats Aggregation                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Export player_data.csv
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                  PYTHON SCRIPTS                             │
│  Script 1: Generate Personalized Cards (PNG)               │
│  Script 2: Generate Personalized HTML Pages                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├─→ personalized_cards/ (100 PNG files)
                 │
                 └─→ wrapped_pages/ (100 HTML files + assets)
                        │
                        │ Drag & drop upload
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                     NETLIFY CDN                             │
│  Hosting: https://cybercom-ctf-wrapped.netlify.app          │
│  - Static file hosting                                      │
│  - Fast global CDN                                          │
│  - Free tier sufficient                                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ URLs generated
                 ↓
┌─────────────────────────────────────────────────────────────┐
│              GOOGLE APPS SCRIPT                             │
│  - Email automation from Google Sheets                      │
│  - Sends personalized emails with unique URLs               │
└─────────────────────────────────────────────────────────────┘
                 │
                 │ Email sent
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    PLAYER                                   │
│  - Receives email                                           │
│  - Clicks unique URL                                        │
│  - Views personalized page                                  │
│  - Shares on social media                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. DATA FLOW

### **Step-by-Step Data Processing**

#### **INPUT: CTF Platform Data**

**Required CSV Exports (from your custom infra):**

**1. users.csv**
```csv
Username,Email,Team,Role,Created_At
alice_123,alice@email.com,Team Red,PLAYER,2026-02-14T10:00:00
bob_456,bob@email.com,Team Blue,PLAYER,2026-02-14T10:15:00
```

**Columns:**
- `Username` - Unique player identifier
- `Email` - For sending wrapped results
- `Team` - Team name (if applicable)
- `Role` - PLAYER/ADMIN/etc
- `Created_At` - Registration timestamp

---

**2. submissions.csv**
```csv
Username,Challenge,Timestamp,Correct,Points,Challenge_Category,Challenge_Act,Time_Spent_Minutes
alice_123,Trust Issues 1,2026-02-14T10:30:00,Yes,100,Trust Issues,Act2,15
alice_123,Stalking 1,2026-02-14T11:00:00,No,0,Stalking,Act1,25
bob_456,Trust Issues 1,2026-02-14T10:45:00,Yes,100,Trust Issues,Act2,20
```

**Columns:**
- `Username` - Player who submitted
- `Challenge` - Challenge name (MUST match challenges sheet)
- `Timestamp` - When submitted
- `Correct` - "Yes" or "No" (case-sensitive!)
- `Points` - Points earned
- `Challenge_Category` - Category name
- `Challenge_Act` - "Act1" or "Act2" (case-sensitive!)
- `Time_Spent_Minutes` - Optional, time on challenge

---

**3. scoreboard.csv**
```csv
Rank,Username,Score,First_Bloods
1,alice_123,4500,3
2,bob_456,4200,1
```

**Columns:**
- `Rank` - Final ranking
- `Username` - Player
- `Score` - Total points
- `First_Bloods` - Number of first bloods

---

#### **PROCESSING: Google Sheets Formulas**

**Google Sheet:** "CTF Wrapped 2025 Master"

**Tabs:**
1. `challenges` - Manual fill before CTF
2. `users` - Import from users.csv
3. `submissions` - Import from submissions.csv
4. `scoreboard` - Import from scoreboard.csv
5. `hints` - Optional manual tracking
6. `CALCULATIONS` - Formulas calculate archetypes
7. `EMAIL_DATA` - Clean final data for export

**Key Formulas in CALCULATIONS Tab (Row 2, drag down):**

```excel
A2: =users!A2                                    // Username
B2: =users!B2                                    // Email
C2: =COUNTIFS(submissions!$A:$A,A2,submissions!$D:$D,"Yes")  // Total Solved
D2: =COUNTA(challenges!$A:$A)-1                  // Total Available
E2: =IF(D2>0,(C2/D2)*100,0)                     // Completion %
F2: =COUNTIFS(submissions!$A:$A,A2,submissions!$D:$D,"Yes",submissions!$G:$G,"Act1")  // Act1 Solved
G2: =COUNTIFS(submissions!$A:$A,A2,submissions!$D:$D,"Yes",submissions!$G:$G,"Act2")  // Act2 Solved
H2: =IF(ISBLANK(hints!A2),0,COUNTIF(hints!$A:$A,A2))  // Hint Count
I2: =IFERROR(INDEX(submissions!$F:$F,MATCH(1,(submissions!$A:$A=A2)*(submissions!$D:$D="Yes"),0)),"N/A")  // Fav Category
J2: =IF(E2=100,"The Committed One",IF(AND(E2>0,E2<50,F2>0,G2=0),"The Heartbreaker",IF(H2>10,"The Overthinker",IF(AND(E2>=80,E2<100),"The Hopeless Romantic",IF(AND(E2>0,E2<70,C2>=5),"The Player",IF(AND(E2>50,G2>F2),"The Slow Burn","The Chaotic Lover"))))))  // Archetype Logic
```

**Archetype Classification Logic:**

```
IF Completion = 100% → The Committed One
ELSE IF Completion < 50% AND Act1 > 0 AND Act2 = 0 → The Heartbreaker
ELSE IF Hints > 10 → The Overthinker  
ELSE IF Completion >= 80% AND < 100% → The Hopeless Romantic
ELSE IF Completion < 70% AND Solved >= 5 → The Player
ELSE IF Completion > 50% AND Act2 > Act1 → The Slow Burn
ELSE → The Chaotic Lover
```

---

#### **OUTPUT: player_data.csv**

Export from EMAIL_DATA tab, contains:

```csv
Username,Email,Archetype,Total_Solved,Total_Available,Rank,Time_Display,Fav_Category,Badges
alice_123,alice@email.com,The Hopeless Romantic,42,50,23,5h 30m,Trust Issues,speed_demon
bob_456,bob@email.com,The Player,35,50,45,3h 15m,Stalking,
```

This CSV drives all card and page generation.

---

## 4. COMPONENTS BREAKDOWN

### **Component 1: Card Generation (Python)**

**Purpose:** Create 100 personalized PNG cards

**Input:**
- `card_bg.png` - Blank template with CYBERCOM branding
- `chibis/` folder - 7 transparent chibi PNGs
- `player_data.csv` - Player stats

**Process:**
1. Load template
2. Determine player's archetype
3. Paste matching chibi character
4. Add archetype title text
5. Add stats text (solved, rank, time, favorite)
6. Save as `{username}_card.png`

**Output:** `personalized_cards/` with 100 PNG files

**Tech:** Python + Pillow (PIL)

---

### **Component 2: Web Page Generation (Python)**

**Purpose:** Create 100 personalized HTML pages

**Input:**
- `wrapped_template.html` - Dark CYBERCOM-styled HTML template
- `personalized_cards/` - Generated card images
- `player_data.csv` - Player stats

**Process:**
1. Load HTML template
2. For each player:
   - Replace `{{USERNAME}}` with actual username
   - Replace `{{ARCHETYPE}}` with archetype name
   - Replace `{{CARD_URL}}` with card image path
   - Replace stats placeholders
   - Add archetype description
   - Generate badges HTML
   - Set share URLs
3. Save as `{username}.html`
4. Copy card image to `wrapped_pages/cards/`

**Output:** `wrapped_pages/` with 100 HTML files + cards subfolder

**Tech:** Python + Pandas + HTML templating

---

### **Component 3: Web Hosting (Netlify)**

**Purpose:** Host all HTML pages publicly

**Process:**
1. Drag `wrapped_pages/` folder to Netlify
2. Site deploys automatically
3. Get URL: `https://cybercom-ctf-wrapped.netlify.app`
4. Each player accessible at: `https://cybercom-ctf-wrapped.netlify.app/{username}.html`

**Tech:** Netlify CDN (free tier)

---

### **Component 4: Email Distribution (Google Apps Script)**

**Purpose:** Send personalized emails to all players

**Input:** Google Sheets EMAIL_DATA tab

**Process:**
1. Script reads EMAIL_DATA
2. For each row (player):
   - Constructs personalized email body
   - Generates unique URL
   - Sends via Gmail API
   - Adds 1 second delay (rate limiting)
3. Logs sent emails

**Output:** 100 emails delivered

**Tech:** Google Apps Script (JavaScript) + Gmail API

---

## 5. FILE STRUCTURE

```
ctf_wrapped/
│
├── card_bg.png                      # Blank card template (1080x1920px)
├── wrapped_template.html            # HTML page template
├── player_data.csv                  # Exported from Google Sheets
│
├── chibis/                          # 7 transparent chibi PNGs
│   ├── chibi_hopeless_romantic.png
│   ├── chibi_player.png
│   ├── chibi_committed_one.png
│   ├── chibi_heartbreaker.png
│   ├── chibi_overthinker.png
│   ├── chibi_chaotic_lover.png
│   └── chibi_slow_burn.png
│
├── personalize_cards_v2.py          # Card generation script
├── generate_html_pages.py           # HTML generation script
│
├── personalized_cards/              # Generated by script 1
│   ├── alice_123_card.png
│   ├── bob_456_card.png
│   └── ... (100 cards)
│
└── wrapped_pages/                   # Generated by script 2
    ├── alice_123.html
    ├── bob_456.html
    ├── ... (100 HTML files)
    └── cards/
        ├── alice_123_card.png
        ├── bob_456_card.png
        └── ... (100 cards copied here)
```

---

## 6. IMPLEMENTATION STEPS

### **Timeline: Feb 15 (8 PM) → Feb 17 (10 AM)**

#### **Feb 15, 8:00 PM - Data Collection**

**Task:** Export data from CTF platform

**Owner:** Tech team

**Steps:**
1. Access CTF platform admin panel
2. Export users → save as `users.csv`
3. Export submissions → save as `submissions.csv`
4. Export scoreboard → save as `scoreboard.csv`
5. Verify CSV formats match specifications
6. Send to non-technical co-founder

**Deliverable:** 3 CSV files

---

#### **Feb 15, 8:30 PM - Data Import**

**Task:** Import CSVs to Google Sheets

**Owner:** Non-technical co-founder (with your help if needed)

**Steps:**
1. Open Google Sheets: "CTF Wrapped 2025 Master"
2. Go to `users` tab → Paste users.csv data
3. Go to `submissions` tab → Paste submissions.csv data
4. Go to `scoreboard` tab → Paste scoreboard.csv data
5. Verify data imported correctly (spot check 5 rows)

**Deliverable:** Populated Google Sheet

---

#### **Feb 15, 9:00 PM - Formula Execution**

**Task:** Calculate archetypes for all players

**Owner:** Automatic (formulas) + verification by non-tech co-founder

**Steps:**
1. Go to `CALCULATIONS` tab
2. Formulas in row 2 should auto-calculate
3. Drag formulas down to last player (row 102 for 100 players)
4. Verify archetypes look reasonable
5. Go to `EMAIL_DATA` tab
6. Drag formulas down to last player
7. Verify all columns populated

**Deliverable:** Calculated archetypes for all players

---

#### **Feb 15, 9:15 PM - Export Final Data**

**Task:** Export clean data as CSV

**Owner:** Non-technical co-founder

**Steps:**
1. In Google Sheets, go to `EMAIL_DATA` tab
2. File → Download → Comma-separated values (.csv)
3. Save as `player_data.csv`
4. Move to `ctf_wrapped/` folder

**Deliverable:** `player_data.csv` file

---

#### **Feb 15, 9:20 PM - Generate Cards**

**Task:** Run Python script to create 100 personalized cards

**Owner:** Tech team

**Prerequisites:**
- Python 3.7+ installed
- `pip install pillow pandas` completed
- All files in place (template, chibis, CSV)

**Steps:**
```bash
cd ctf_wrapped
python personalize_cards_v2.py
```

**Expected Output:**
```
============================================================
CTF CARD PERSONALIZER V2 - TEMPLATE BASED
============================================================

📊 Reading player data from player_data.csv...
  ✓ Found 100 players

🎨 Generating personalized cards...
------------------------------------------------------------
  ✓ Generated card for alice_123 (The Hopeless Romantic)
  ✓ Generated card for bob_456 (The Player)
  ... (100 lines)
------------------------------------------------------------

✅ COMPLETE!
   Successfully generated: 100 cards
   
📁 Cards saved to: personalized_cards/
============================================================
```

**Validation:**
- Check `personalized_cards/` folder has 100 PNG files
- Open 5 random cards, verify they look correct
- Check text is readable, chibi is positioned correctly

**Deliverable:** 100 personalized card PNGs

**Time:** ~5-10 minutes

---

#### **Feb 15, 9:30 PM - Generate HTML Pages**

**Task:** Run Python script to create 100 personalized web pages

**Owner:** Tech team

**Steps:**
```bash
cd ctf_wrapped
python generate_html_pages.py
```

**Expected Output:**
```
============================================================
CTF WRAPPED HTML GENERATOR
============================================================

📄 Reading HTML template...
  ✓ Template loaded

📊 Reading player data from player_data.csv...
  ✓ Found 100 players

🎨 Generating personalized pages...
------------------------------------------------------------
  ✓ Generated page for alice_123
  ✓ Generated page for bob_456
  ... (100 lines)
------------------------------------------------------------

✅ COMPLETE!
   Successfully generated: 100 pages

📁 Pages saved to: wrapped_pages/
   Card images in: wrapped_pages/cards/

📤 NEXT STEPS:
   1. Go to https://app.netlify.com/drop
   2. Drag the 'wrapped_pages' folder onto the page
   ... (instructions)
============================================================
```

**Validation:**
- Check `wrapped_pages/` has 100 HTML files
- Check `wrapped_pages/cards/` has 100 PNG files
- Open `alice_123.html` in browser locally
- Verify page displays correctly

**Deliverable:** 100 HTML pages + assets

**Time:** ~5 minutes

---

#### **Feb 15, 9:40 PM - Deploy to Netlify**

**Task:** Upload pages to web hosting

**Owner:** Tech team or non-tech co-founder

**Steps:**
1. Go to https://app.netlify.com (sign up if needed - free)
2. Click "Add new site" → "Deploy manually"
3. Drag entire `wrapped_pages/` folder onto upload area
4. Wait 2 minutes for deployment
5. Netlify shows: "Your site is live at: https://random-name-12345.netlify.app"
6. Click "Site settings" → "Change site name"
7. Set to: `cybercom-ctf-wrapped`
8. New URL: `https://cybercom-ctf-wrapped.netlify.app`
9. Test: Open `https://cybercom-ctf-wrapped.netlify.app/alice_123.html`
10. Verify page loads, card displays, stats correct

**Deliverable:** Live website with all pages

**Time:** ~5 minutes

---

#### **Feb 15, 9:50 PM - Update Share URLs**

**Task:** Re-generate HTML with correct URLs for social sharing

**Owner:** Tech team

**Steps:**
1. Open `generate_html_pages.py` in text editor
2. Find line: `BASE_URL = "https://your-site.netlify.app"`
3. Change to: `BASE_URL = "https://cybercom-ctf-wrapped.netlify.app"`
4. Save file
5. Run again: `python generate_html_pages.py`
6. Re-upload `wrapped_pages/` to Netlify (drag again)
7. Test social share button - verify URL is correct

**Deliverable:** Updated pages with correct share URLs

**Time:** ~5 minutes

---

#### **Feb 15, 10:00 PM - Set Up Email System**

**Task:** Configure automated email sending

**Owner:** Tech team + non-tech co-founder

**Steps:**

1. Open Google Sheets: "CTF Wrapped 2025 Master"
2. Click **Extensions → Apps Script**
3. Delete any existing code
4. Paste the email script (see Code section below)
5. Click **Save** (Ctrl+S)
6. Name: "CTF Wrapped Emailer"

**Test with ONE email:**
7. Modify line: `for (var i = 1; i < data.length; i++)`
8. Change to: `for (var i = 1; i < 2; i++)` (only first player)
9. Click **Run**
10. Authorize permissions (Google will prompt)
11. Check first player's email - did they receive it?
12. Click link in email - does it work?
13. If yes, change back to: `for (var i = 1; i < data.length; i++)`

**Schedule for Feb 17:**
14. Click **Triggers** (clock icon on left)
15. Click **+ Add Trigger**
16. Function: `sendCTFWrapped`
17. Event: Time-driven
18. Type: Specific date and time
19. Date: Feb 17, 2026
20. Time: 10:00 AM
21. Click **Save**

**Deliverable:** Email system ready, scheduled to send Feb 17 10 AM

**Time:** ~30 minutes

---

#### **Feb 15, 10:30 PM - Final Validation**

**Task:** End-to-end testing

**Owner:** Both tech team + non-tech co-founder

**Checklist:**
- [ ] All 100 cards generated correctly
- [ ] All 100 HTML pages exist
- [ ] Netlify site is live
- [ ] Random sample of 10 pages load correctly
- [ ] Cards display properly
- [ ] Stats are accurate (compare to Google Sheet)
- [ ] Share buttons work
- [ ] Download button works
- [ ] Email test successful
- [ ] Email scheduled for Feb 17 10 AM

**Deliverable:** Validated, ready-to-launch system

**Time:** ~15 minutes

---

#### **Feb 16 - Buffer Day**

Optional day for:
- Fixing any issues found
- Preparing social media posts
- Creating feedback form
- Double-checking everything

---

#### **Feb 17, 10:00 AM - LAUNCH!**

**Task:** Emails send automatically

**Owner:** Automated (monitor for issues)

**What happens:**
1. Google Apps Script trigger fires at 10 AM
2. Emails send to all 100 players (~2 minutes total)
3. Players receive emails, click links
4. Traffic flows to Netlify site
5. Social sharing begins!

**Monitoring:**
- Check Google Sheets Apps Script logs for errors
- Monitor Netlify analytics for traffic
- Watch social media for shares
- Respond to any player questions

**Deliverable:** Successful launch! 🎉

---

## 7. CODE & SCRIPTS

### **Script 1: personalize_cards_v2.py**

```python
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

CSV_FILE = "player_data.csv"
TEMPLATE_BG = "card_bg.png"
CHIBI_FOLDER = "chibis"
OUTPUT_FOLDER = "personalized_cards"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Chibi mapping
CHIBI_MAP = {
    "The Hopeless Romantic": "chibi_hopeless_romantic.png",
    "The Player": "chibi_player.png",
    "The Committed One": "chibi_committed_one.png",
    "The Heartbreaker": "chibi_heartbreaker.png",
    "The Overthinker": "chibi_overthinker.png",
    "The Chaotic Lover": "chibi_chaotic_lover.png",
    "The Slow Burn": "chibi_slow_burn.png"
}

# Text positions (adjust to match your template)
TITLE_POSITION = (540, 280)
TITLE_FONT_SIZE = 68
TITLE_COLOR = (255, 255, 255)

CHIBI_POSITION = (540, 600)
CHIBI_SIZE = (400, 400)

STATS_START_Y = 950
STATS_LINE_HEIGHT = 60
STATS_X = 150
STATS_FONT_SIZE = 40
STATS_COLOR = (255, 255, 255)

# ============================================
# FUNCTIONS
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
    total = str(player_data['Total_Available'])
    rank = str(player_data['Rank'])
    time_display = str(player_data['Time_Display'])
    category = str(player_data['Fav_Category'])
    
    try:
        card = Image.open(template_path).convert('RGBA')
    except FileNotFoundError:
        print(f"  ❌ Template not found: {template_path}")
        return None
    
    chibi_filename = CHIBI_MAP.get(archetype)
    if chibi_filename:
        chibi_path = os.path.join(chibi_folder, chibi_filename)
        try:
            chibi = Image.open(chibi_path).convert('RGBA')
            chibi = chibi.resize(CHIBI_SIZE, Image.Resampling.LANCZOS)
            chibi_x = CHIBI_POSITION[0] - CHIBI_SIZE[0] // 2
            chibi_y = CHIBI_POSITION[1] - CHIBI_SIZE[1] // 2
            card.paste(chibi, (chibi_x, chibi_y), chibi)
        except FileNotFoundError:
            print(f"  ⚠️  Chibi not found: {chibi_path}")
    
    draw = ImageDraw.Draw(card)
    
    try:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
        stats_font = ImageFont.truetype(FONT_PATH, STATS_FONT_SIZE)
    except:
        title_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
    
    add_text_centered(draw, archetype.upper(), TITLE_POSITION, title_font, TITLE_COLOR)
    
    stats_y = STATS_START_Y + STATS_LINE_HEIGHT + 20
    
    add_text_left(draw, f"► SOLVED: {solved}/{total}", (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► RANK: #{rank}", (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► TIME: {time_display}", (STATS_X, stats_y), stats_font, STATS_COLOR)
    stats_y += STATS_LINE_HEIGHT
    
    add_text_left(draw, f"► FAVORITE: {category}", (STATS_X, stats_y), stats_font, STATS_COLOR)
    
    card = card.convert('RGB')
    output_path = os.path.join(output_folder, f"{username}_card.png")
    card.save(output_path, "PNG")
    
    print(f"  ✓ Generated card for {username} ({archetype})")
    return output_path

def main():
    print("=" * 60)
    print("CTF CARD PERSONALIZER V2 - TEMPLATE BASED")
    print("=" * 60)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    if not os.path.exists(TEMPLATE_BG):
        print(f"\n❌ ERROR: Template not found: {TEMPLATE_BG}")
        return
    
    if not os.path.exists(CHIBI_FOLDER):
        print(f"\n❌ ERROR: Chibi folder not found: {CHIBI_FOLDER}")
        return
    
    print(f"\n📊 Reading player data from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"  ✓ Found {len(df)} players")
    except FileNotFoundError:
        print(f"  ❌ Error: File '{CSV_FILE}' not found!")
        return
    
    print(f"\n🎨 Generating personalized cards...")
    print("-" * 60)
    
    generated_count = 0
    failed_count = 0
    
    for index, row in df.iterrows():
        player_data = row.to_dict()
        result = personalize_card(player_data, TEMPLATE_BG, CHIBI_FOLDER, OUTPUT_FOLDER)
        if result:
            generated_count += 1
        else:
            failed_count += 1
    
    print("-" * 60)
    print(f"\n✅ COMPLETE!")
    print(f"   Successfully generated: {generated_count} cards")
    if failed_count > 0:
        print(f"   Failed: {failed_count} cards")
    print(f"\n📁 Cards saved to: {OUTPUT_FOLDER}/")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

### **Script 2: generate_html_pages.py**

*(See previously provided script - too long to repeat here, but it's in the files)*

**Key sections:**
- Reads `player_data.csv`
- Loads `wrapped_template.html`
- Replaces placeholders: `{{USERNAME}}`, `{{ARCHETYPE}}`, etc.
- Generates badges HTML
- Adds archetype descriptions
- Saves as `{username}.html`
- Copies card images

---

### **Script 3: Google Apps Script (Email)**

```javascript
function sendCTFWrapped() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("EMAIL_DATA");
  var data = sheet.getDataRange().getValues();
  
  // Start from row 2 (skip header)
  for (var i = 1; i < data.length; i++) {
    var username = data[i][0];  // Column A
    var email = data[i][1];     // Column B
    
    var wrappedURL = "https://cybercom-ctf-wrapped.netlify.app/" + username + ".html";
    
    var subject = "Your Valentine's CTF Wrapped is Here! 💘";
    
    var body = "Hi " + username + ",\n\n" +
      "Thank you for participating in CYBERCOM's Valentine's Day CTF!\n\n" +
      "Your personalized CTF Wrapped is ready:\n" +
      "👉 " + wrappedURL + "\n\n" +
      "Discover your hacker archetype, view your stats, and share your results!\n\n" +
      "See you at the next CTF!\n\n" +
      "CYBERCOM Team\n" +
      "#CYBERCOMValentineCTF";
    
    MailApp.sendEmail({
      to: email,
      subject: subject,
      body: body
    });
    
    Logger.log('Sent to: ' + email);
    Utilities.sleep(1000); // 1 second delay
  }
  
  Logger.log('All emails sent!');
}
```

---

## 8. TESTING & VALIDATION

### **Test Cases**

**Test 1: Card Generation**
- Input: Test CSV with 5 players, all different archetypes
- Expected: 5 PNG cards, each with correct chibi and stats
- Validation: Open each card, verify text readable, chibi correct

**Test 2: HTML Generation**
- Input: Same test CSV
- Expected: 5 HTML files with correct data
- Validation: Open in browser, verify stats match CSV

**Test 3: Netlify Deployment**
- Input: Test HTML files
- Expected: All pages accessible via URLs
- Validation: Open 5 URLs, all load correctly

**Test 4: Email Sending**
- Input: Test CSV with YOUR email 5 times (different usernames)
- Expected: 5 emails received with unique URLs
- Validation: Click each link, verify goes to correct page

---

## 9. DEPLOYMENT

### **Deployment Checklist**

**Pre-Deployment:**
- [ ] All 100 cards generated
- [ ] All 100 HTML pages generated
- [ ] Sample validation passed (10 random pages checked)
- [ ] Netlify site live
- [ ] Email system tested
- [ ] Email scheduled for Feb 17 10 AM

**Deployment:**
- [ ] Final upload to Netlify
- [ ] DNS propagation verified (all pages load)
- [ ] Social share buttons tested
- [ ] Download buttons tested
- [ ] Email trigger confirmed

**Post-Deployment:**
- [ ] Monitor email sends (Feb 17 10 AM)
- [ ] Check Netlify analytics
- [ ] Watch social media
- [ ] Respond to feedback
- [ ] Collect analytics data

---

## 10. TROUBLESHOOTING

### **Common Issues & Solutions**

**Issue: Cards have wrong text positions**
- **Cause:** Template positions don't match script positions
- **Fix:** Adjust `TITLE_POSITION`, `STATS_START_Y` values in script
- **How:** Open card_bg.png, measure pixel positions, update script

**Issue: Chibis not showing on cards**
- **Cause:** Chibis not in correct folder or wrong filenames
- **Fix:** Verify `chibis/` folder has all 7 PNGs with exact names
- **Names:** Must match `CHIBI_MAP` dictionary in script

**Issue: Chibis have visible backgrounds**
- **Cause:** PNGs not truly transparent
- **Fix:** Use remove.bg or regenerate with transparent background
- **Verify:** Open PNG in image viewer, background should be checkered

**Issue: Emails not sending**
- **Cause:** Gmail API permissions not granted
- **Fix:** Re-run script, authorize all permissions Google requests
- **Alternative:** Use Mailchimp for email sending instead

**Issue: Netlify deployment fails**
- **Cause:** Folder too large (>100MB)
- **Fix:** Compress card images or use Netlify with account (higher limits)

**Issue: HTML pages show broken images**
- **Cause:** Card images not in `wrapped_pages/cards/` folder
- **Fix:** Verify script copied images, or manually copy `personalized_cards/` to `wrapped_pages/cards/`

**Issue: Share buttons don't work**
- **Cause:** BASE_URL not updated in script
- **Fix:** Update `BASE_URL` in `generate_html_pages.py`, regenerate, re-upload

**Issue: Formulas return #N/A or 0**
- **Cause:** Data not imported correctly, capitalization mismatch
- **Fix:** Verify "Yes"/"No" and "Act1"/"Act2" capitalization in submissions.csv

---

## ADDITIONAL RESOURCES

### **Required Software**

- Python 3.7+ with pip
- Pillow: `pip install pillow`
- Pandas: `pip install pandas`
- Google account (for Sheets & Gmail)
- Netlify account (free tier)
- Text editor (VS Code, Sublime, etc.)

### **File Downloads**

All scripts and templates available in project folder:
- `personalize_cards_v2.py`
- `generate_html_pages.py`
- `wrapped_template.html`
- `card_bg.png`
- Chibi PNGs (to be generated)

### **Documentation Links**

- Pillow docs: https://pillow.readthedocs.io/
- Pandas docs: https://pandas.pydata.org/docs/
- Netlify docs: https://docs.netlify.com/
- Google Apps Script: https://developers.google.com/apps-script

---

## CONTACT & SUPPORT

**Questions During Implementation:**
- Slack/Discord: [Your team channel]
- Email: [Tech team email]
- Emergency: [Phone number]

**Roles:**
- Tech Team: Card/HTML generation, deployment, troubleshooting
- Non-Tech Co-Founder: Data import, Google Sheets, project management
- Both: Testing, validation, launch monitoring

---

## SUCCESS METRICS

**Primary Goals:**
- 100% email delivery rate
- >80% email open rate
- >50% click-through rate (to wrapped pages)
- >20% social share rate

**Secondary Goals:**
- Zero critical errors during launch
- Positive player feedback
- Increased social media engagement
- Data collection for next CTF improvement

---

## CONCLUSION

This system automates the creation of 100 personalized CTF result experiences, from data processing through card generation to email delivery.

**Total automated time:** ~15 minutes to generate all content
**Total manual time:** ~2 hours for setup, testing, deployment
**Player impact:** Memorable, shareable post-event experience

**Key success factors:**
1. Clean data export from CTF platform
2. Accurate Google Sheets formulas
3. Quality chibi images (transparent backgrounds)
4. Proper text positioning on cards
5. Thorough testing before launch

**Go build something awesome! 🚀**

---

*Last updated: Feb 14, 2026*
*Version: 1.0*
*Author: Technical documentation for CYBERCOM CTF Wrapped system*
