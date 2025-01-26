import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict, Counter
from dotenv import load_dotenv

# Ladda API-nyckeln från .env
load_dotenv()
API_KEY = os.getenv("FACEIT_API_KEY")

# Endast dessa kartor analyseras
VALID_MAPS = {"Mirage", "Train", "Nuke", "Ancient", "Anubis", "Inferno", "Dust 2"}

# Initiera Flask-servern
app = Flask(__name__)
CORS(app)  # Möjliggör API-anrop från Chrome Extension

def get_match_details(room_id):
    """Hämtar matchdetaljer för att få alla spelare och lag."""
    url = f"https://open.faceit.com/data/v4/matches/{room_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Fel vid hämtning av matchdetaljer: {response.status_code}")
        return None

def get_player_most_played_maps(player_id, nickname):
    """Hämtar en spelares mest spelade kartor, även kartor med 0 matcher."""
    url = f"https://open.faceit.com/data/v4/players/{player_id}/stats/cs2"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        stats = response.json()
        segments = stats.get("segments", [])

        # Initiera alla kartor med 0 spelade matcher
        map_stats = {map_name: (0, 0.0) for map_name in VALID_MAPS}

        for segment in segments:
            if segment["type"] == "Map":
                map_name = segment["label"]
                if map_name in VALID_MAPS:
                    matches = int(segment["stats"].get("Matches", 0))
                    win_rate = float(segment["stats"].get("Win Rate %", 0))
                    map_stats[map_name] = (matches, win_rate)

        # Om ingen karta har spelats, returnera 0 på alla kartor
        sorted_maps = sorted(map_stats.items(), key=lambda x: x[1][0])  # Sortera baserat på matcher spelade
        
        return {
            "nickname": nickname,
            "maps": [{"map": map_name, "matches": matches, "win_rate": win_rate} for map_name, (matches, win_rate) in sorted_maps]
        }
    
    return None

def analyze_ban_probability(players_maps):
    """Analyserar sannolikheten för bans per lag, även för spelare som aldrig spelat en karta."""
    map_counter = Counter()
    map_players = defaultdict(list)
    map_match_count = defaultdict(int)  # Totalt antal spelade matcher per karta

    for player_nickname, maps in players_maps.items():
        if maps:
            least_played_map = min(maps["maps"], key=lambda x: x["matches"])  # Hämta den minst spelade kartan
            map_counter[least_played_map["map"]] += 1  # Räkna hur många som har den som minst spelad
            map_players[least_played_map["map"]].append(player_nickname)  # Lägg till spelaren under kartan

            # Lägg till matchräkning för varje karta
            for map_info in maps["maps"]:
                map_match_count[map_info["map"]] += map_info["matches"]

    return map_counter, map_players, map_match_count

@app.route("/analyze", methods=["GET"])
def analyze_match():
    """Analyserar Faceit-matchen och returnerar en JSON med data."""
    room_id = request.args.get("room_id")
    if not room_id:
        return jsonify({"error": "Room ID saknas"}), 400

    match_data = get_match_details(room_id)
    if not match_data:
        return jsonify({"error": "Misslyckades att hämta matchdata"}), 500

    teams = match_data.get("teams", {})
    team_players = {}
    team_names = {}

    # Hämta spelare per lag
    for team_key, team in teams.items():
        team_name = team["name"]
        team_names[team_key] = team_name
        team_players[team_key] = [(player["player_id"], player["nickname"]) for player in team["roster"]]

    team_maps_data = {}

    # Hämta kartdata för varje spelare
    for team_key, players in team_players.items():
        players_maps = {}
        for player_id, player_nickname in players:
            maps = get_player_most_played_maps(player_id, player_nickname)
            if maps:
                players_maps[player_nickname] = maps  # Använd spelarens nickname istället för ID

        team_maps_data[team_key] = players_maps

    # Analysera bans per lag
    team_analysis = {}
    for team_key, players_maps in team_maps_data.items():
        ban_probabilities, map_players, map_match_counts = analyze_ban_probability(players_maps)

        team_analysis[team_key] = {
            "team_name": team_names[team_key],
            "ban_probabilities": [{"map": map_name, "count": count, "players": map_players[map_name]} for map_name, count in ban_probabilities.most_common()],
            "map_match_counts": [{"map": map_name, "matches": match_count} for map_name, match_count in sorted(map_match_counts.items(), key=lambda x: x[1])]
        }

    return jsonify({
        "teams": team_names,
        "players_maps": team_maps_data,
        "team_analysis": team_analysis
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

