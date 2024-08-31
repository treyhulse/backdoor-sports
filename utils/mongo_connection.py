from pymongo import MongoClient
import streamlit as st

def get_mongo_connection():
    # Connect to MongoDB using the connection string from secrets
    client = MongoClient(st.secrets["mongo_uri"])
    db = client['backdoor_sports']  # Replace with your database name
    return db
