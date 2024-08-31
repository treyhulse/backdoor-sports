# 02_Player_Page.py

import streamlit as st
from utils.mongo_connection import get_mongo_connection
import requests

# Load API key from secrets
api_key = st.secrets["cfb_api_key"]

st.title("🏈 Player Stats")

# Get search term from the user
search_term = st.text_input("Search for a Player")

# Fetch player names based on search term
if search_term:
    response = requests.get(
        f"https://api.collegefootballdata.com/player/search?searchTerm={search_term}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    players = response.json()

    # Handle potential errors in the response
    if "error" in players:
        st.error(f"Error: {players['error']}")
    elif len(players) == 0:
        st.warning("No players found. Please try another name.")
    else:
        player_names = [f"{player['first_name']} {player['last_name']}" for player in players]
        selected_player = st.selectbox("Select a Player", player_names)

        if st.button("Get Player Stats"):
            # Get the selected player's ID
            player_data = next(player for player in players if f"{player['first_name']} {player['last_name']}" == selected_player)

            # Fetch player stats
            url = f"https://api.collegefootballdata.com/player/stats?year=2024&id={player_data['id']}"
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(url, headers=headers)
            player_stats = response.json()

            if player_stats:
                st.write(f"### Stats for {selected_player}")
                st.write(f"Passing Yards: {player_stats[0].get('passing_yards', 'N/A')}")
                st.write(f"Rushing Yards: {player_stats[0].get('rushing_yards', 'N/A')}")
                st.write(f"Receiving Yards: {player_stats[0].get('receiving_yards', 'N/A')}")
            else:
                st.write("No stats found for this player.")

# Section to display top 10 QBs, RBs, and WRs
st.write("## Top 10 Players by Position")

# Fetch all player stats and filter by position
url = f"https://api.collegefootballdata.com/player/seasonStats?year=2024"
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get(url, headers=headers)
all_players_stats = response.json()

def display_top_players_by_position(position, stat_key, title):
    top_players = sorted(
        [player for player in all_players_stats if player['position'] == position],
        key=lambda x: x.get(stat_key, 0),
        reverse=True
    )[:10]

    st.write(f"### Top 10 {title}")
    for player in top_players:
        st.write(f"{player['first_name']} {player['last_name']} - {player[stat_key]} {title}")

display_top_players_by_position("QB", "passing_yards", "Passing Yards")
display_top_players_by_position("RB", "rushing_yards", "Rushing Yards")
display_top_players_by_position("WR", "receiving_yards", "Receiving Yards")
