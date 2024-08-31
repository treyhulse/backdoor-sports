import streamlit as st
import requests

# Load API key from secrets
api_key = st.secrets["api"]["cfb_api_key"]

st.title("🏈 Teams and Matchups")

team_name = st.text_input("Enter Team Name", value="Alabama")
week = st.number_input("Enter Week Number", min_value=1, max_value=15, value=1)

if st.button("Get Team Matchups"):
    # API call to get team matchups
    url = f"https://api.collegefootballdata.com/games"
    params = {
        'year': 2024,
        'week': week,
        'team': team_name
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers, params=params)
    matchups = response.json()

    if matchups:
        st.write(f"### Matchups for {team_name} - Week {week}")
        for game in matchups:
            st.write(f"{game['home_team']} vs {game['away_team']} - {game['start_date']}")
            st.write(f"Final Score: {game['home_points']} - {game['away_points']}")
    else:
        st.write("No matchups found for the specified team and week.")
