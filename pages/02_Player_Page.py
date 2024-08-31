import streamlit as st
import requests
import time

# Load API key from secrets
api_key = st.secrets["cfb_api_key"]

st.title("🏈 Player Stats")

player_name = st.text_input("Enter Player Name", value="John Doe")
team_name = st.text_input("Enter Team Name", value="Alabama")

if st.button("Get Player Stats"):
    progress_bar = st.progress(0)

    # Simulate loading progress
    for i in range(1, 101):
        time.sleep(0.01)
        progress_bar.progress(i)

    # API call to get player stats
    url = f"https://api.collegefootballdata.com/player/stats"
    params = {
        'year': 2024,
        'team': team_name,
        'seasonType': 'regular'
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers, params=params)
    player_stats = response.json()

    if player_stats:
        st.write(f"### Stats for {player_name} - {team_name}")
        for player in player_stats:
            if player['name'].lower() == player_name.lower():
                st.write(f"Passing Yards: {player['passing_yards']}")
                st.write(f"Rushing Yards: {player['rushing_yards']}")
                st.write(f"Touchdowns: {player['touchdowns']}")
                break
        else:
            st.write("Player not found in the provided team.")
    else:
        st.write("No stats found for the specified player.")
