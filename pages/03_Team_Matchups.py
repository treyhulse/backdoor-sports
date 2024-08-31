import streamlit as st
import requests
import datetime

# Load API key from secrets
api_key = st.secrets["cfb_api_key"]

# Function to determine the current week based on today's date
def get_current_week():
    start_date = datetime.date(2024, 8, 24)  # Assuming the season starts on Aug 24, 2024
    today = datetime.date.today()
    delta = today - start_date
    current_week = delta.days // 7 + 1
    return max(1, min(current_week, 15))  # Season should have between 1 and 15 weeks

st.title("🏈 College Football Scoreboard")

# Automatically determine the current week and set the week selection
current_week = get_current_week()
week = st.selectbox("Select Week", options=[f"Week {i}" for i in range(1, 16)], index=current_week-1)

# Filters
conference = st.selectbox("Select Conference", options=["All", "SEC", "Big Ten", "Pac-12", "ACC", "Big 12"])
team_ranking = st.selectbox("Select Team Ranking", options=["All", "Top 25", "Top 10", "Unranked"])
game_status = st.selectbox("Select Game Status", options=["All", "Old", "Live", "Future"])

st.write(f"Showing matchups for {week}")

# Progress bar for loading data
progress_bar = st.progress(0)

# Simulate loading progress
for i in range(1, 101):
    progress_bar.progress(i)

# API call to get game results for the top 25 teams
url = f"https://api.collegefootballdata.com/games"
params = {
    'year': 2024,
    'week': int(week.split()[1]),
    'ranked': True if team_ranking != "Unranked" else False
}
headers = {
    'Authorization': f'Bearer {api_key}'
}
response = requests.get(url, headers=headers, params=params)
matchups = response.json()

# Apply additional filters (conference, game status)
filtered_matchups = []
for game in matchups:
    if (conference == "All" or conference in game['home_conference'] or conference in game['away_conference']) and \
       (game_status == "All" or
        (game_status == "Old" and datetime.datetime.strptime(game['start_date'], "%Y-%m-%dT%H:%M:%S%z").date() < datetime.date.today()) or
        (game_status == "Live" and game['status'] == "in_progress") or
        (game_status == "Future" and datetime.datetime.strptime(game['start_date'], "%Y-%m-%dT%H:%M:%S%z").date() > datetime.date.today())):
        filtered_matchups.append(game)

# Display matchups
if filtered_matchups:
    st.write(f"### Top 25 Matchups - {week}")
    for game in filtered_matchups:
        st.markdown(
            f"""
            <div style="padding: 10px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); margin-bottom: 15px; background-color: #ffffff;">
                <div style="display: flex; justify-content: space-between;">
                    <div style="width: 15%;">
                        <img src="https://a.espncdn.com/i/teamlogos/ncaa/500/{game['home_id']}.png" style="height: 50px;"/>
                        <p style="font-size: 18px; font-weight: bold;">{game['home_team']} vs {game['away_team']}</p>
                        <img src="https://a.espncdn.com/i/teamlogos/ncaa/500/{game['away_id']}.png" style="height: 50px;"/>
                    </div>
                    <div style="width: 15%;">
                        <p style="font-size: 18px; font-weight: bold;">{game['home_points']} - {game['away_points']}</p>
                    </div>
                    <div style="width: 40%;">
                        <p>Last Play: {game.get('last_play', 'N/A')}</p>
                        <div style="display: flex; justify-content: space-between;">
                            <div>PASS: {game.get('pass_leader', {}).get('name', 'N/A')}</div>
                            <div>RUSH: {game.get('rush_leader', {}).get('name', 'N/A')}</div>
                            <div>REC: {game.get('rec_leader', {}).get('name', 'N/A')}</div>
                        </div>
                    </div>
                    <div style="width: 15%; text-align: right;">
                        <a href="#" style="margin-right: 10px;">Watch</a>
                        <a href="#">Gamecast</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.write("No matchups found for the specified filters.")
