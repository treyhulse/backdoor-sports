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

            # Fetch player stats using the correct endpoint
            url = f"https://api.collegefootballdata.com/stats/player/season?year=2024&id={player_data['id']}"
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(url, headers=headers)
            player_stats = response.json()

            if player_stats:
                st.write(f"### Stats for {selected_player}")
                grouped_stats = {}
                for stat_entry in player_stats:
                    stat_type = stat_entry.get('statType')
                    stat_value = stat_entry.get('stat')
                    grouped_stats[stat_type] = stat_value

                st.write(f"Passing Yards: {grouped_stats.get('YDS', 'N/A')}")  # Update key based on the actual stat type
                st.write(f"Rushing Yards: {grouped_stats.get('YDS', 'N/A')}")  # Same key as passing; modify as needed
                st.write(f"Receiving Yards: {grouped_stats.get('YDS', 'N/A')}")  # Same key as above; modify as needed
            else:
                st.write("No stats found for this player.")

# Section to display top 10 QBs, RBs, and WRs
st.write("## Top 10 Players by Position")

# Fetch all player stats by position using the correct endpoint
url = "https://api.collegefootballdata.com/stats/player/season?year=2024"
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get(url, headers=headers)

# Check if the response is successful and contains valid JSON
if response.status_code == 200:
    try:
        all_players_stats = response.json()
        st.write("Fetched player stats successfully.")
        st.write("Sample of the API response:", all_players_stats[:5])  # Show the first 5 entries for inspection
    except ValueError as e:
        st.error(f"Error decoding JSON: {e}")
        st.write("Response content:", response.text)
else:
    st.error(f"Failed to fetch player stats: {response.status_code}")
    st.write("Response content:", response.text)

def display_top_players_by_position(stat_type, title):
    if 'all_players_stats' in locals():
        # Filter the players by stat type and sort by the value of the stat
        top_players = sorted(
            [player for player in all_players_stats if player.get('statType') == stat_type],
            key=lambda x: float(x.get('stat', 0)),
            reverse=True
        )[:10]

        if top_players:
            st.write(f"### Top 10 {title}")
            for player in top_players:
                st.write(f"{player['player']} ({player['team']}) - {player.get('stat', 'N/A')} {title}")
        else:
            st.write(f"No data available to display for {title}")
    else:
        st.write(f"No data available to display for {title}")

# Display top players by stat category
display_top_players_by_position("YDS", "Rushing Yards")  # Update the key as needed for each category
