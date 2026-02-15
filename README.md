# 🎉 CTF Wrapped - Amor Mortis Valentine's Day CTF 2025

**"Spotify Wrapped" style personalized results system for CTF competitions**

![CYBERCOM CTF](https://img.shields.io/badge/CYBERCOM-CTF%20Wrapped-orange)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📖 Overview

A complete automated system to create personalized "wrapped" experiences for CTF participants, similar to Spotify Wrapped. Each player receives:

- 🎴 **Personalized card** with their unique "hacker archetype"
- 📊 **Custom stats** (challenges solved, rank, time, favorite category)
- 🏆 **Badges** for special achievements
- 🌐 **Personal webpage** with shareable results
- 📱 **Social media integration** (Twitter, LinkedIn, Facebook)

**Built for:** CYBERCOM's Valentine's Day CTF 2025 "Amor Mortis"
**Players:** 163 participants
**Archetypes:** 7 unique personality types based on solving behavior

---

## ✨ Features

### 🎨 Automated Card Generation
- Python script generates 163 unique PNG cards
- Each card includes chibi character matching archetype
- Stats overlay (solved, rank, time, category)
- Dark cyberpunk Valentine theme
- Downloadable 1080x1920px cards

### 🌐 Personal Web Pages
- 163 individual HTML pages
- Beautiful dark CYBERCOM-styled design
- Responsive mobile-first layout
- Share buttons with Open Graph meta tags
- Smooth animations and transitions

### 🤖 Player Archetype System
Automatically classifies players into 7 archetypes based on behavior:

1. **🌈 The Chaotic Lover** - Unpredictable, energetic approach
2. **💔 The Heartbreaker** - Started strong, then ghosted
3. **🎮 The Player** - Strategic, efficient solver
4. **🤔 The Overthinker** - Analytical, methodical
5. **🔥 The Slow Burn** - Steady improvement over time
6. **🏔️ The Committed One** - Never gave up, 100% completion
7. **💘 The Hopeless Romantic** - Patient, dedicated, 80%+ completion

### 📧 Email Distribution
- Automated email system via Google Apps Script
- Personalized messages with unique URLs
- Rate-limited sending (1/second)
- Error handling and logging

---

## 🏗️ Architecture

```
CTF Platform (users, submissions, scores)
            ↓
    process_ctf_data.py (data transformation)
            ↓
      player_data.csv (163 players)
            ↓
    ┌──────────────────────┐
    ↓                      ↓
personalize_cards_v2.py   generate_html_pages.py
    ↓                      ↓
personalized_cards/    wrapped_pages/
(163 PNG files)        (163 HTML files)
            ↓
        Netlify CDN (hosting)
            ↓
    Google Apps Script (email)
            ↓
        163 Players
```

---

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/balakumaran1507/Amor_Motis_Nabi_Project.git
cd Amor_Motis_Nabi_Project

# Create virtual environment
python3 -m venv ctf_venv
source ctf_venv/bin/activate  # On Windows: ctf_venv\Scripts\activate

# Install dependencies
pip install pillow pandas

# You're ready!
```

---

## 🚀 Usage

### Step 1: Prepare Your Data

Export 3 CSV files from your CTF platform:
1. `users.csv` - All registered users
2. `submissions.csv` - All challenge submissions
3. `scoreboard.csv` - Final team rankings

### Step 2: Process Data

```bash
python process_ctf_data.py
```

This generates `player_data.csv` with calculated archetypes.

### Step 3: Customize Design

Place your design assets:
- `card_bg.png` - Card template (1080x1920px)
- `chibis/` - 7 transparent PNG chibi characters

Or use placeholders:
```bash
python create_placeholders.py
```

### Step 4: Generate Cards

```bash
python personalize_cards_v2.py
```

Output: `personalized_cards/` folder with 163 PNG files

### Step 5: Generate Web Pages

```bash
python generate_html_pages.py
```

Output: `wrapped_pages/` folder with 163 HTML files + assets

### Step 6: Deploy

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag `wrapped_pages/` folder
3. Get your URL (e.g., `https://your-site.netlify.app`)

### Step 7: Update Share Links

1. Edit `generate_html_pages.py` line 23
2. Set `BASE_URL = "https://your-actual-url.netlify.app"`
3. Re-run `python generate_html_pages.py`
4. Re-upload to Netlify

### Step 8: Send Emails

See `DEPLOYMENT_GUIDE.md` for complete email setup instructions.

---

## 📂 Project Structure

```
.
├── README.md                      # This file
├── DEPLOYMENT_GUIDE.md            # Step-by-step deployment
├── TECH_TEAM_DOCUMENTATION.md     # Technical deep dive
│
├── process_ctf_data.py            # Transform CTF exports → player_data.csv
├── personalize_cards_v2.py        # Generate PNG cards
├── generate_html_pages.py         # Generate HTML pages
├── create_placeholders.py         # Create test assets
│
├── wrapped_template.html          # HTML page template
├── card_bg.png                    # Card background template
├── chibis/                        # 7 chibi character PNGs
│   ├── chibi_chaotic_lover.png
│   ├── chibi_heartbreaker.png
│   ├── chibi_player.png
│   ├── chibi_overthinker.png
│   ├── chibi_slow_burn.png
│   ├── chibi_committed_one.png
│   └── chibi_hopeless_romantic.png
│
└── .gitignore                     # Git ignore rules
```

**Generated (not in repo):**
```
personalized_cards/    # 163 PNG cards
wrapped_pages/         # 163 HTML pages + assets
player_data.csv        # Player data with emails (sensitive)
```

---

## ⚙️ Configuration

### `personalize_cards_v2.py`

```python
# Input files
CSV_FILE = "player_data.csv"
TEMPLATE_BG = "card_bg.png"
CHIBI_FOLDER = "chibis"

# Output
OUTPUT_FOLDER = "personalized_cards"

# Design (adjust to match your template)
TITLE_POSITION = (540, 280)       # Archetype title
CHIBI_POSITION = (540, 600)       # Chibi character center
STATS_START_Y = 950               # Stats box Y position
```

### `generate_html_pages.py`

```python
# Input
CSV_FILE = "player_data.csv"
HTML_TEMPLATE = "wrapped_template.html"
CARDS_FOLDER = "personalized_cards"

# Output
OUTPUT_FOLDER = "wrapped_pages"
BASE_URL = "https://your-site.netlify.app"  # Update after deploy
```

---

## 🎨 Customization

### Change Archetypes

Edit `process_ctf_data.py` function `calculate_archetype()`:

```python
def calculate_archetype(stats):
    completion = stats['completion_percent']

    if completion == 100:
        return "The Committed One"
    elif completion >= 80:
        return "The Hopeless Romantic"
    # Add your own logic...
```

### Modify Card Design

1. Create new `card_bg.png` (1080x1920px)
2. Adjust positions in `personalize_cards_v2.py`:
   - `TITLE_POSITION`
   - `CHIBI_POSITION`
   - `STATS_START_Y`

### Update HTML Styling

Edit `wrapped_template.html` CSS variables:

```css
:root {
    --bg-primary: #0a0a0a;
    --orange: #FF6B35;
    /* Add your colors */
}
```

---

## 📊 Data Format

### Input: `player_data.csv`

```csv
Username,Email,Archetype,Total_Solved,Total_Available,Rank,Time_Display,Fav_Category,Badges
alice,alice@email.com,The Player,8,22,5,11h 38m,Cryptography,speed_demon
bob,bob@email.com,The Heartbreaker,3,22,18,4h 23m,Web,
```

**Required columns:**
- `Username` - Unique identifier
- `Email` - For sending wrapped links
- `Archetype` - One of 7 types
- `Total_Solved` - Challenges completed
- `Total_Available` - Total challenges in CTF
- `Rank` - Final ranking
- `Time_Display` - Formatted time (e.g., "5h 30m")
- `Fav_Category` - Most attempted category
- `Badges` - Comma-separated (optional)

---

## 🌐 Live Example

**Deployed Site:** `https://cybercom-ctf-wrapped.netlify.app`

**Example URLs:**
- `https://cybercom-ctf-wrapped.netlify.app/LUFFY.html`
- `https://cybercom-ctf-wrapped.netlify.app/bat.html`

---

## 📈 Results

**CYBERCOM Valentine's CTF 2025:**
- ✅ **163 players** received personalized wrapped
- ✅ **5 archetypes** represented
- ✅ **17MB** total deployment size
- ✅ **~30 min** generation time (all cards + pages)

**Archetype Distribution:**
- 🌈 The Chaotic Lover: 80 (49%)
- 💔 The Heartbreaker: 66 (40%)
- 🎮 The Player: 12 (7%)
- 🤔 The Overthinker: 4 (2%)
- 🔥 The Slow Burn: 1 (1%)

---

## 🔧 Troubleshooting

### Card Generation Issues

**Problem:** Chibis not appearing
- **Solution:** Ensure PNG files are transparent and filenames match exactly

**Problem:** Text overlapping
- **Solution:** Adjust `TITLE_POSITION` and `STATS_START_Y` values

### HTML Generation Issues

**Problem:** Cards not loading on pages
- **Solution:** Verify `cards/` folder was created in `wrapped_pages/`

**Problem:** Share buttons broken
- **Solution:** Update `BASE_URL` and regenerate pages

### Deployment Issues

**Problem:** Netlify upload fails
- **Solution:** Check folder size < 100MB, compress images if needed

---

## 📝 License

MIT License - Feel free to use for your own CTF events!

---

## 🙏 Acknowledgments

**Created by:** CYBERCOM Team
**Event:** Valentine's Day CTF 2025 - "Amor Mortis"
**Inspired by:** Spotify Wrapped
**Tech Stack:** Python, Pillow, Pandas, Netlify, Google Apps Script

---

## 🤝 Contributing

Improvements welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

**Ideas for improvements:**
- [ ] Add more archetype logic options
- [ ] Create web-based configuration UI
- [ ] Add analytics dashboard
- [ ] Support multiple languages
- [ ] Video card generation

---

## 📧 Contact

**Questions?** Open an issue or contact:
- **GitHub:** [@balakumaran1507](https://github.com/balakumaran1507)
- **Project:** CYBERCOM

---

## 🎯 Next CTF?

Planning to use this for your CTF? Here's the quick checklist:

- [ ] Clone repository
- [ ] Install dependencies
- [ ] Export your CTF data (3 CSV files)
- [ ] Run `process_ctf_data.py`
- [ ] Customize card design
- [ ] Generate cards & pages
- [ ] Deploy to Netlify
- [ ] Send emails to participants
- [ ] Watch the engagement roll in! 🎉

---

**⭐ Star this repo if you found it useful!**

**Made with ❤️ for the CTF community**
