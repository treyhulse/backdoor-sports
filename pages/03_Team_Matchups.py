import streamlit as st
import requests
import time

# Load API key from secrets
api_key = st.secrets["cfb_api_key"]

st.title("🏈 Teams and Matchups")

# Week selection at the top right
st.markdown(
    """
    <style>
    .css-18e3th9 {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

week = st.selectbox("Select Week", options=[f"Week {i}" for i in range(1, 16)], index=0)

if st.button("Get Top 25 Matchups"):
    progress_bar = st.progress(0)

    # Simulate loading progress
    for i in range(1, 101):
        time.sleep(0.01)
        progress_bar.progress(i)

    # API call to get game results for the top 25 teams
    url = f"https://api.collegefootballdata.com/games"
    params = {
        'year': 2024,
        'week': int(week.split()[1]),
        'ranked': True
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers, params=params)
    matchups = response.json()

    if matchups:
        st.write(f"### Top 25 Matchups - {week}")
        for game in matchups:
            # Display game details as cards
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); margin-bottom: 15px;">
                    <h3>{game['home_team']} vs {game['away_team']}</h3>
                    <p>Date: {game['start_date']}</p>
                    <p>Final Score: {game['home_points']} - {game['away_points']}</p>
                    <p>Location: {game['venue']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No matchups found for the specified week.")
