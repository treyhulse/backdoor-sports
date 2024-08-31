import streamlit as st

st.set_page_config(
    page_title="College Football Fantasy App",
    page_icon="🏈",
    layout="wide"
)

st.sidebar.title("Navigation")
st.sidebar.markdown("## Select a page:")
page = st.sidebar.selectbox("", ["Homepage", "Player Page", "Teams/Matchups"])

if page == "Homepage":
    st.write("### Welcome to the College Football Fantasy App!")
    st.write("Explore the latest stats, players, teams, and matchups.")
    st.image("https://via.placeholder.com/800x400?text=College+Football+Fantasy", use_column_width=True)
    st.write("Navigate through the sidebar to view different sections of the app.")

elif page == "Player Page":
    st.write("Player Page")

elif page == "Teams/Matchups":
    st.write("Teams/Matchups Page")
