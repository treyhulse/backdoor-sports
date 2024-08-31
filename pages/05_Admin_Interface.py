# 05_Admin_Interface.py

import streamlit as st
from utils.mongo_connection import get_mongo_connection
from utils.auth import authenticate_user, check_permission
import datetime

# Get the MongoDB connection
db = get_mongo_connection()
accounts_collection = db['accounts']
bets_collection = db['bets']
permissions_collection = db['permissions']
roles_collection = db['roles']

st.title("🏈 Admin - Make a Bet")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

user = authenticate_user(username, password)
if user:
    st.write(f"Welcome {user['username']}!")
    
    # Check if the user has permission to post bets
    if check_permission(user, "post_bets"):
        # Bet details
        team_1 = st.text_input("Team 1", value="")
        team_2 = st.text_input("Team 2", value="")
        bet_type = st.selectbox("Bet Type", options=["Moneyline", "Spread", "Total", "Prop Bet"])
        odds = st.text_input("Odds", value="")
        amount = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Date", value=datetime.date.today())

        if st.button("Post Bet"):
            # Insert the new bet into MongoDB
            bet = {
                "team_1": team_1,
                "team_2": team_2,
                "bet_type": bet_type,
                "odds": odds,
                "amount": amount,
                "date": str(date),
                "status": "posted",
                "created_by": user['username']
            }
            bets_collection.insert_one(bet)
            st.success("Bet posted successfully!")
    else:
        st.error("You do not have permission to post bets.")
else:
    st.error("Invalid username or password.")
