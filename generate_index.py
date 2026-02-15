#!/usr/bin/env python3
"""Generate index.html with all players"""

import pandas as pd
import json

# Read player data
df = pd.read_csv("../player_data.csv")

# Convert to JavaScript array
players_data = []
for _, row in df.iterrows():
    players_data.append({
        "username": row['Username'],
        "archetype": row['Archetype'],
        "solved": row['Total_Solved'],
        "rank": row['Rank'],
        "time": row['Time_Display']
    })

# Generate JavaScript code
js_data = json.dumps(players_data, indent=8)

# HTML template
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBERCOM CTF Wrapped 2025 - All Players</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --orange: #FF6B35;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --border: #333333;
        }}

        body {{
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 2px solid var(--orange);
        }}

        h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: -2px;
        }}

        .subtitle {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            color: var(--orange);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}

        .stat-box {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 20px;
            text-align: center;
        }}

        .stat-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--orange);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}

        .search-box {{
            margin: 40px 0;
        }}

        input[type="text"] {{
            width: 100%;
            padding: 16px 20px;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}

        input[type="text"]:focus {{
            outline: none;
            border-color: var(--orange);
        }}

        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 10px 20px;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .filter-btn:hover, .filter-btn.active {{
            border-color: var(--orange);
            background: var(--orange);
            color: var(--bg-primary);
        }}

        .player-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}

        .player-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 20px;
            transition: all 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: var(--text-primary);
            display: block;
        }}

        .player-card:hover {{
            border-color: var(--orange);
            transform: translateY(-4px);
        }}

        .player-name {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        .player-archetype {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            color: var(--orange);
            margin-bottom: 15px;
        }}

        .player-stats {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        .player-stats div {{
            margin: 5px 0;
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
        }}

        footer {{
            text-align: center;
            margin-top: 80px;
            padding-top: 40px;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>CYBERCOM</h1>
            <p class="subtitle">CTF Wrapped 2025 - Amor Mortis</p>
        </header>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Total Users</div>
                <div class="stat-value" id="total-players">166</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Archetypes</div>
                <div class="stat-value">5</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Challenges</div>
                <div class="stat-value">22</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Status</div>
                <div class="stat-value" style="font-size: 1.5rem; color: var(--orange);">LIVE</div>
            </div>
        </div>

        <div class="search-box">
            <input type="text" id="search" placeholder="🔍 Search by username...">
        </div>

        <div class="filter-buttons">
            <button class="filter-btn active" data-filter="all">All Users</button>
            <button class="filter-btn" data-filter="The Chaotic Lover">🌈 Chaotic Lover (83)</button>
            <button class="filter-btn" data-filter="The Heartbreaker">💔 Heartbreaker (66)</button>
            <button class="filter-btn" data-filter="The Player">🎮 Player (12)</button>
            <button class="filter-btn" data-filter="The Overthinker">🤔 Overthinker (4)</button>
            <button class="filter-btn" data-filter="The Slow Burn">🔥 Slow Burn (1)</button>
        </div>

        <div class="player-grid" id="player-grid"></div>

        <footer>
            <p>CYBERCOM Valentine's Day CTF 2025</p>
            <p style="margin-top: 10px; color: var(--orange);">#CYBERCOMValentineCTF</p>
        </footer>
    </div>

    <script>
        // Player data - ALL 166 USERS
        const players = {js_data};

        const playerGrid = document.getElementById('player-grid');
        const searchInput = document.getElementById('search');
        const filterBtns = document.querySelectorAll('.filter-btn');
        let currentFilter = 'all';

        function renderPlayers(filteredPlayers) {{
            if (filteredPlayers.length === 0) {{
                playerGrid.innerHTML = '<div class="no-results">No players found matching your criteria.</div>';
                return;
            }}

            playerGrid.innerHTML = filteredPlayers.map(player => `
                <a href="${{player.username}}.html" class="player-card">
                    <div class="player-name">${{player.username}}</div>
                    <div class="player-archetype">${{player.archetype}}</div>
                    <div class="player-stats">
                        <div>► Solved: ${{player.solved}}/22</div>
                        <div>► Rank: #${{player.rank}}</div>
                        <div>► Time: ${{player.time}}</div>
                    </div>
                </a>
            `).join('');

            document.getElementById('total-players').textContent = filteredPlayers.length;
        }}

        function filterPlayers() {{
            const searchTerm = searchInput.value.toLowerCase();
            let filtered = players;

            if (currentFilter !== 'all') {{
                filtered = filtered.filter(p => p.archetype === currentFilter);
            }}

            if (searchTerm) {{
                filtered = filtered.filter(p => p.username.toLowerCase().includes(searchTerm));
            }}

            filtered.sort((a, b) => a.username.localeCompare(b.username));
            renderPlayers(filtered);
        }}

        searchInput.addEventListener('input', filterPlayers);

        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                filterPlayers();
            }});
        }});

        // Initial render
        filterPlayers();
    </script>
</body>
</html>'''

# Write to file
with open("../wrapped_pages/index.html", "w") as f:
    f.write(html)

print("✅ Index page generated with all 166 users!")
print(f"📊 Total users: {len(players_data)}")
print("\nArchetype breakdown:")
for archetype in ["The Chaotic Lover", "The Heartbreaker", "The Player", "The Overthinker", "The Slow Burn"]:
    count = sum(1 for p in players_data if p['archetype'] == archetype)
    print(f"  • {archetype}: {count}")
