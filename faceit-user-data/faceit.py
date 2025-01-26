import requests
import os
from dotenv import load_dotenv

# Laddar API-nyckeln från .env
load_dotenv()

def get_faceit_user_info(username, api_key):
    """Hämtar Faceit-användarinformation baserat på username."""
    url = f"https://open.faceit.com/data/v4/players?nickname={username}"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fel vid hämtning av användardata: {response.status_code}")
        return None

def get_latest_match_stats(player_id, game_id, api_key):
    """Hämtar senaste matchens statistik för en spelare."""
    url = f"https://open.faceit.com/data/v4/players/{player_id}/stats/{game_id}"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fel vid hämtning av matchstatistik: {response.status_code}")
        return None

if __name__ == "__main__":
    api_key = os.getenv("FACEIT_API_KEY")  # Hämta API-nyckeln från .env
    
    if not api_key:
        print("API-nyckel saknas! Se till att du har angett den i .env.")
    else:
        username = input("Ange Faceit-användarnamn: ")  # Användaren skriver in sitt namn
        user_info = get_faceit_user_info(username, api_key)

        if user_info:
            # Hämta player_id
            player_id = user_info.get("player_id", None)
            if player_id:
                print(f"Hittade Player ID: {player_id}")

                # Hämta senaste matchens statistik för CS2
                game_id = "cs2"
                match_stats = get_latest_match_stats(player_id, game_id, api_key)

                if match_stats:
                    print(f"\n🎯 Senaste matchens statistik för {username}:")
                    
                    # Hämta viktiga stats från "lifetime"
                    lifetime_stats = match_stats.get("lifetime", {})
                    print(f"✅ Total Kills: {lifetime_stats.get('Total Kills with extended stats', 'N/A')}")
                    print(f"✅ K/D Ratio: {lifetime_stats.get('K/D Ratio', 'N/A')}")
                    print(f"✅ Headshot %: {lifetime_stats.get('Total Headshots %', 'N/A')}")
                    print(f"✅ ADR (Average Damage per Round): {lifetime_stats.get('ADR', 'N/A')}")
                    print(f"✅ Win Rate %: {lifetime_stats.get('Win Rate %', 'N/A')}")
                    print(f"✅ Matches Spelade: {lifetime_stats.get('Total Matches', 'N/A')}")
                    
                    # Hämta senaste resultat (1=vinst, 0=förlust)
                    recent_results = lifetime_stats.get("Recent Results", [])
                    recent_results_str = " ".join(["✅" if r == "1" else "❌" for r in recent_results])
                    print(f"🏆 Senaste matcher: {recent_results_str}")

                else:
                    print("Kunde inte hämta matchstatistik.")
            else:
                print("Kunde inte hitta Player ID.")
        else:
            print("Misslyckades med att hämta användarinformation.")
