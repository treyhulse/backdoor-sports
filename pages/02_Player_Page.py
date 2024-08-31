# 02_Player_Page.py

import streamlit as st
from utils.mongo_connection import get_mongo_connection
import requests

# Load API key from secrets
api_key = st.secrets["cfb_api_key"]

st.title("🏈 Team Stats")

# Fetch all team stats by season using the correct endpoint
url = "https://api.collegefootballdata.com/stats/player/season?year=2024"
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get(url, headers=headers)

# Check if the response is successful and contains valid JSON
if response.status_code == 200:
    try:
        all_teams_stats = response.json()
        st.write("Fetched team stats successfully.")
        st.write("Sample of the API response:", all_teams_stats[:5])  # Show the first 5 entries for inspection
    except ValueError as e:
        st.error(f"Error decoding JSON: {e}")
        st.write("Response content:", response.text)
else:
    st.error(f"Failed to fetch team stats: {response.status_code}")
    st.write("Response content:", response.text)

def display_top_teams_by_stat(stat_type, title):
    if 'all_teams_stats' in locals():
        # Aggregate stats by team and stat type
        team_stats = {}
        for entry in all_teams_stats:
            team = entry.get('team')
            stat_value = float(entry.get('stat', 0))
            if entry.get('statType') == stat_type:
                if team not in team_stats:
                    team_stats[team] = 0
                team_stats[team] += stat_value

        # Sort teams by the aggregated stat value
        sorted_teams = sorted(team_stats.items(), key=lambda x: x[1], reverse=True)[:10]

        if sorted_teams:
            st.write(f"### Top 10 Teams by {title}")
            for team, stat_value in sorted_teams:
                st.write(f"{team} - {stat_value} {title}")
        else:
            st.write(f"No data available to display for {title}")
    else:
        st.write(f"No data available to display for {title}")

# Display top teams by different stat categories
display_top_teams_by_stat("YDS", "Total Yards")  # Modify as needed for different categories
display_top_teams_by_stat("TD", "Touchdowns")
display_top_teams_by_stat("CAR", "Carries")
