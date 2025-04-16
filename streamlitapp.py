import streamlit as st
import requests
import json

# Define the base URL of your Flask server
BASE_URL = "http://localhost:5000"

# Function to make GET requests to Flask server
def get_data(endpoint):
    response = requests.get(BASE_URL + endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def insert_player(player_data):
    response = post_data("/insertPlayer", {"data": json.dumps(player_data)})
    return response
# Function to make POST requests to Flask server
def post_data(endpoint, data):
    response = requests.post(BASE_URL + endpoint, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title("IPL MANAGEMENT SYSTEM")

    # Menu options
    menu = ["Home", "View Teams", "Add Team", "View Players", "Add Player"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the Grocery Store Management System!")

    elif choice == "View Teams":
        st.subheader("All Teams")
        teams = get_data("/getTeam")
        if teams:
            for team in teams:
                st.write(f"Team Name: {team['team_name']}, Total Players: {team['total_players']}, Team Owner: {team['team_owner']}")
        else:
            st.write("No teams available.")

    elif choice == "Add Team":
        st.subheader("Add New Team")
        team_id = st.number_input("Team ID", min_value=1)
        team_name = st.text_input("Team Name")
        total_players = st.number_input("Total Players", min_value=0)
        total_purse = st.number_input("Total Purse", min_value=0.0)
        team_owner = st.text_input("Team Owner")
        if st.button("Add"):
            if team_id is not None and team_name and total_players is not None and total_purse is not None and team_owner:
                response = post_data("/insertTeam", {"data": json.dumps({
                    "team_id": team_id,
                    "team_name": team_name,
                    "total_players": total_players,
                    "total_purse": total_purse,
                    "team_owner": team_owner
                })})
                if response:
                    st.success(f"Team '{team_name}' added successfully!")
                else:
                    st.error("Failed to add team.")
            else:
                st.warning("Please enter all team details.")

    elif choice == "View Players":
        st.subheader("All Players")
        players = get_data("/getAllPlayer")
        if players:
            for player in players:
                st.write(f"Player Name: {player['player_name']}, Team: {player['team_name']}, Age: {player['player_age']}")
                st.write("Player Details:")
                for detail in player['player_details']:
                    st.write(f"Total Runs: {detail['total_run']}, Total Wickets: {detail['total_wicket']}, Price: {detail['price']}")
                st.write("---")
        else:
            st.write("No players available.")

    elif choice == "Add Player":
        st.subheader("Add New Player")
        team_id = st.number_input("Team ID", min_value=1)
        player_id = st.number_input("Player ID", min_value=1)
        player_name = st.text_input("Player Name")
        player_age = st.number_input("Player Age", min_value=0)
        total_runs = st.number_input("Total Runs", min_value=0)
        total_wickets = st.number_input("Total Wickets", min_value=0)
        price = st.number_input("Price", min_value=0.0)

        player_data = {
            "team_id": team_id,
            "player_id": player_id,
            "player_name": player_name,
            "player_age": player_age,
            "player_detail": [{
                "total_run": total_runs,
                "total_wicket": total_wickets,
                "price": price
            }]
        }

        if st.button("Add Player"):
            response = insert_player(player_data)
            if response:
                st.success(f"Player '{player_name}' added successfully!")
            else:
                st.error("Failed to add player.")

if __name__ == "__main__":
    main()
