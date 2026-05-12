import os
import json 
import requests
from bs4 import BeautifulSoup
import time

# Essential headers to avoid being blocked by Transfermarkt
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
}

BASE_URL = "https://www.transfermarkt.com"

# Mapping Transfermarkt position names to the shorthand the game expects
POSITION_MAPPING = {
    "Goalkeeper": "GK",
    "Centre-Back": "CB",
    "Left-Back": "LB",
    "Right-Back": "RB",
    "Defensive Midfield": "CDM",
    "Central Midfield": "CM",
    "Attacking Midfield": "CAM",
    "Left Winger": "LW",
    "Right Winger": "RW",
    "Centre-Forward": "ST",
    "Second Striker": "SS",
}

# Cache for team squad data (to avoid fetching the same team multiple times)
# Structure: { team_id: { player_name: jersey_number } }
team_squad_cache = {}

def get_team_numbers(team_id):
    """Fetches the squad page for a team and returns a mapping of player names to their jersey numbers."""
    if team_id in team_squad_cache:
        return team_squad_cache[team_id]
        
    print(f"  --> Fetching jersey numbers for Team ID {team_id}...")
    url = f"{BASE_URL}/team/kader/verein/{team_id}"
    try:
        time.sleep(1) # Small delay before team fetch
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        numbers = {}
        squad_table = soup.find("table", class_="items")
        if squad_table:
            tbody = squad_table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr", class_=["odd", "even"], recursive=False)
                for row in rows:
                    name_td = row.find("td", class_="hauptlink")
                    num_div = row.find("div", class_="rn_nummer")
                    if name_td and num_div:
                        # Extract the actual name text inside the link
                        name_a = name_td.find("a")
                        name = name_a.get_text(strip=True) if name_a else name_td.get_text(strip=True)
                        num_str = num_div.get_text(strip=True)
                        try:
                            numbers[name] = int(num_str)
                        except:
                            numbers[name] = 0
                            
        team_squad_cache[team_id] = numbers
        return numbers
    except Exception as e:
        print(f"      Error fetching team {team_id}: {e}")
        return {}

def get_top_valued_players(page=1):
    """Scrapes the Super Lig market values page for the most valuable players."""
    print(f"Fetching Top Market Values from Page {page}...")
    # The ajax URL works better for pagination
    url = f"{BASE_URL}/super-lig/marktwerte/wettbewerb/TR1/ajax/yw1/page/{page}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch market values: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    players = []
    
    table = soup.find("table", class_="items")
    if not table:
        print("Could not find the market values table.")
        return players
        
    tbody = table.find("tbody")
    if not tbody:
        return players
        
    rows = tbody.find_all("tr", class_=["odd", "even"], recursive=False)
    
    for row in rows:
        try:
            # 1. Name & Position
            # Name is in a 'hauptlink' class inside an inline table
            name_td = row.find("td", class_="hauptlink")
            if not name_td: continue
            name = name_td.find("a").get_text(strip=True)
            
            # Position is in the second row of the inline table
            inline_table = row.find("table", class_="inline-table")
            position_text = "Unknown"
            if inline_table:
                p_rows = inline_table.find_all("tr")
                if len(p_rows) > 1:
                    position_text = p_rows[1].get_text(strip=True)

            # 2. All zentriert cells contain: Rank, Flag(Nationality), Age, Club Logo
            zentriert_tds = row.find_all("td", class_="zentriert")
            
            # Nationality (Cell index 2)
            nat_td = zentriert_tds[1]
            img_nat = nat_td.find("img", class_="flaggenrahmen")
            nationality = img_nat["title"] if img_nat else "Unknown"

            # Age (Cell index 3)
            age_td = zentriert_tds[2]
            try:
                age = int(age_td.get_text(strip=True))
            except:
                age = 0

            # Club (Cell index 4)
            club_td = zentriert_tds[3]
            club_a = club_td.find("a")
            club_name = club_a["title"] if club_a and club_a.has_attr("title") else "Unknown"
            club_link = club_a["href"] if club_a else ""
            # Link looks like: /galatasaray-istanbul/startseite/verein/141/saison_id/2025
            club_id = ""
            if "/verein/" in club_link:
                parts = club_link.split("/")
                club_id = parts[parts.index("verein") + 1]

            # 3. Jersey Number (Lookup from team cache)
            team_numbers = get_team_numbers(club_id) if club_id else {}
            number = team_numbers.get(name, 0)

            # Map position
            position_shorthand = POSITION_MAPPING.get(position_text, position_text)
            
            players.append({
                "name": name,
                "age": age,
                "nationality": nationality,
                "club": club_name,
                "position": position_shorthand,
                "number": number
            })
        except Exception as e:
            # print(f"Error parsing row: {e}")
            continue
            
    return players

def main():
    # Fetch top 50 (2 pages of 25)
    all_players = []
    all_players.extend(get_top_valued_players(page=1))
    all_players.extend(get_top_valued_players(page=2))

    if not all_players:
        print("\nNo players were fetched. Transfermarkt might be blocking your requests.")
        return

    # Take the top 50
    final_players = all_players[:50]

    filepath = os.path.join(os.path.dirname(__file__), "players.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(final_players, f, indent=4, ensure_ascii=False)
    
    print(f"\nSuccessfully updated {filepath} with the Top 50 most valued players in the Super League!")
    print("Here are the top 5 players added:")
    for p in final_players[:5]:
        print(f"- {p['name']} ({p['club']}) - Age: {p['age']} - #{p['number']}")

if __name__ == "__main__":
    main()
