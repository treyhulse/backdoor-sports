# utils/mongo_connection.py

from pymongo import MongoClient
import streamlit as st

def get_mongo_connection():
    """
    Establish a connection to MongoDB using the connection string stored in Streamlit secrets.
    
    Returns:
    - db: The MongoDB database connection.
    """
    client = MongoClient(st.secrets["mongo_uri"])
    db = client['backdoor_sports']  # Replace with your database name
    return db
