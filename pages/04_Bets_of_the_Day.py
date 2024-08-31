# 04_Bets_of_the_Day.py

import streamlit as st
from utils.mongo_connection import get_mongo_connection

# Get the MongoDB connection
db = get_mongo_connection()
bets_collection = db['bets']

st.title("🏈 Bets of the Day")

# Fetch the bets from MongoDB
bets = bets_collection.find({"status": "posted"})

if bets.count() > 0:
    for bet in bets:
        st.markdown(
            f"""
            <div style="padding: 10px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); margin-bottom: 15px; background-color: #ffffff;">
                <h3>{bet['team_1']} vs {bet['team_2']}</h3>
                <p><strong>Bet:</strong> {bet['bet_type']}</p>
                <p><strong>Odds:</strong> {bet['odds']}</p>
                <p><strong>Amount:</strong> {bet['amount']}</p>
                <p><strong>Date:</strong> {bet['date']}</p>
                <p><strong>Created by:</strong> {bet['created_by']}</p>
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.write("No bets have been posted for today.")
