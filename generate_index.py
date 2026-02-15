#!/usr/bin/env python3
"""Generate index.html with all players using built-in csv module"""

import csv
import json
import os

# Get paths
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "player_data.csv")

# Read player data
players_data = []
try:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            players_data.append({
                "username": row['Username'],
                "archetype": row['Archetype'],
                "solved": row['Total_Solved'],
                "rank": row['Rank'],
                "time": row['Time_Display']
            })
except FileNotFoundError:
    print(f"❌ Error: {csv_path} not found")
    exit(1)

# Generate JavaScript code
js_data = json.dumps(players_data, indent=8)

# HTML template
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBERCOM CTF Wrapped 2025 - All Operatives</title>
    <link rel="stylesheet" href="globals.css">
    <style>
        .player-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
        .player-card {{
            border: 1px solid var(--border);
            padding: 24px;
            text-decoration: none;
            color: var(--foreground);
            transition: var(--transition);
            background: rgba(255,255,255,0.01);
            position: relative;
        }}
        .player-card:hover {{
            background: rgba(255,255,255,0.03);
            border-color: var(--accent);
            transform: translateY(-4px);
        }}
        .player-name {{
            font-family: var(--font-display);
            font-size: 1.5rem;
            margin-bottom: 5px;
            letter-spacing: 0.05em;
        }}
        .player-archetype {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--accent);
            margin-bottom: 20px;
        }}
        .player-stats {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            opacity: 0.7;
        }}
        .player-stats div {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 15px 20px;
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            color: var(--foreground);
            font-family: var(--font-mono);
            font-size: 0.9rem;
            margin: 40px 0;
            transition: var(--transition);
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: var(--accent);
            background: rgba(255,255,255,0.05);
        }}
        .filter-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }}
        .no-results {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 80px;
            border: 1px dashed var(--border);
            font-family: var(--font-mono);
            opacity: 0.5;
        }}
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="glow-overlay"></div>

    <div class="container fade-in" style="padding: 100px 0;">
        <header style="text-align: center; margin-bottom: 80px;">
            <div class="mono-tag" style="margin-bottom: 20px;">► OPERATIVE_DATABASE_V1.0</div>
            <h1 class="header-display" style="font-size: 5rem;">CYBERCOM</h1>
            <p class="mono-tag">CTF WRAPPED // AMOR MORTIS // 2025</p>
        </header>

        <div class="search-container">
            <input type="text" id="search" placeholder="[ SEARCH_OPERATIVE_ID ]">
        </div>

        <div class="filter-buttons">
            <button class="btn-cyber active" data-filter="all">ALL_FILES</button>
            <button class="btn-cyber" data-filter="The Chaotic Lover">CHAOTIC_LOVER</button>
            <button class="btn-cyber" data-filter="The Heartbreaker">HEARTBREAKER</button>
            <button class="btn-cyber" data-filter="The Player">PLAYER</button>
            <button class="btn-cyber" data-filter="The Overthinker">OVERTHINKER</button>
            <button class="btn-cyber" data-filter="The Slow Burn">SLOW_BURN</button>
        </div>

        <div class="player-grid" id="player-grid"></div>

        <footer style="margin-top: 100px; text-align: center; border-top: 1px solid var(--border); padding-top: 60px;">
            <p class="mono-tag">CLASSIFIED // FOR AUTHORIZED PERSONNEL ONLY</p>
        </footer>
    </div>

    <script>
        const players = {js_data};
        const playerGrid = document.getElementById('player-grid');
        const searchInput = document.getElementById('search');
        const filterBtns = document.querySelectorAll('.filter-buttons .btn-cyber');
        let currentFilter = 'all';

        function renderPlayers(filteredPlayers) {{
            if (filteredPlayers.length === 0) {{
                playerGrid.innerHTML = '<div class="no-results">SYSTEM_ERROR: NO MATCHING RECORDS FOUND</div>';
                return;
            }}

            playerGrid.innerHTML = filteredPlayers.map(player => `
                <a href="${{player.username}}.html" class="player-card">
                    <div class="player-name">${{player.username}}</div>
                    <div class="player-archetype">${{player.archetype}}</div>
                    <div class="player-stats">
                        <div><span>SOLVED</span> <span>${{player.solved}}/22</span></div>
                        <div><span>RANK</span> <span>#${{player.rank}}</span></div>
                        <div><span>TIME</span> <span>${{player.time}}</span></div>
                    </div>
                </a>
            `).join('');
        }}

        function filterPlayers() {{
            const searchTerm = searchInput.value.toLowerCase().trim();
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

        filterPlayers();
    </script>
</body>
</html>'''

# Write to file
output_dir = os.path.join(base_path, "wrapped_pages")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, "index.html")
with open(output_path, "w") as f:
    f.write(html)

print(f"✅ Index page generated successfully at {output_path}")
