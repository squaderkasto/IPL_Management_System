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

# Function to make POST requests to Flask server
def post_data(endpoint, data):
    response = requests.post(BASE_URL + endpoint, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def insert_player(player_data):
    response = post_data("/insertPlayer", {"data": json.dumps(player_data)})
    return response

def insert_match(match_data):
    response = post_data("/insertMatch", {"data": json.dumps(match_data)})
    return response

def delete_match(team_name):
    response = post_data("/deleteMatch", {"team_name": team_name})
    return response

def update_points_db(team_name, wins, losses, point):
    response = post_data("/updatePoints", {"data": json.dumps({
        "team_name": team_name,
        "wins": wins,
        "losses": losses,
        "point": point
    })})
    return response

def view_points_table():
    points_data = get_data("/viewPoints")
    return points_data

def main():
    st.title("IPL MANAGEMENT SYSTEM")

    # Menu options
    menu = ["Home", "View Teams", "Add Team", "View Players", "Add Player", "Add Match", "Delete Match", "Update Points", "View Points Table"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the IPL Management System!")

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

    elif choice == "Add Match":
        st.subheader("Add New Match")
        team_name = st.text_input("Team Name")
        team_id = st.number_input("Team ID", min_value=1)
        wins = st.number_input("Wins", min_value=0)
        losses = st.number_input("Losses", min_value=0)
        point = st.number_input("Points", min_value=0)
        if st.button("Add Match"):
            match_data = {
                "team_name": team_name,
                "team_id": team_id,
                "wins": wins,
                "losses": losses,
                "point": point
            }
            response = insert_match(match_data)
            if response:
                st.success("Match inserted successfully")
            else:
                st.error("Failed to add match.")

    elif choice == "Delete Match":
        st.subheader("Delete Match")
        team_name = st.text_input("Team Name")
        if st.button("Delete Match"):
            response = delete_match(team_name)
            if response:
                st.success("Match deleted successfully")
            else:
                st.error("Failed to delete match.")
    
    elif choice == "Update Points":
        st.subheader("Update Points for a Team")
        team_name = st.text_input("Team Name")
        wins = st.number_input("Wins", min_value=0)
        losses = st.number_input("Losses", min_value=0)
        point = st.number_input("Points", min_value=0)
        if st.button("Update Points"):
            response = update_points_db(team_name, wins, losses, point)
            if response:
                 st.success("Points updated successfully")
            else:
                 st.error("Failed to update points.")
    
    elif choice == "View Points Table":
        st.subheader("Points Table")
        points_data = view_points_table()
        if points_data:
            import pandas as pd
            df=pd.DataFrame(points_data)
            st.write(df)
        else:
            st.write("Failed to fetch points data.")

if __name__ == "__main__":
    main()
