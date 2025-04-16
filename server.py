from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json

import teams
import players
import matches
app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getTeam', methods=['GET'])
def get_teams():
    response = teams.get_all_teams(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertTeam', methods=['POST'])
def insert_team():
    request_payload = json.loads(request.form['data'])
    team_id = teams.insert_new_team(connection, request_payload)
    response = jsonify({
        'team_id': team_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllPlayer', methods=['GET'])
def get_all_players():
    response = players.get_all_players(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertPlayer', methods=['POST'])
def insert_player():
    request_payload = json.loads(request.form['data'])
    player_id = players.insert_player(connection, request_payload)
    response = jsonify({
        'player': player_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertPlayerDetail', methods=['POST'])
def insert_player_detail():
    request_payload = json.loads(request.form['data'])
    player_detail_id = players.insert_player_detail(connection, request_payload)
    response = jsonify({
        'player_detail_id': player_detail_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertMatch', methods=['POST'])
def insert_match():
    request_payload = json.loads(request.form['data'])
    team_name = request_payload.get('team_name')
    team_id = request_payload.get('team_id')
    wins = request_payload.get('wins')
    losses = request_payload.get('losses')
    point = request_payload.get('point')

    matches.insert_row(team_name, team_id, wins, losses, point)

    response = jsonify({
        'message': 'Match inserted successfully'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteMatch', methods=['POST'])
def delete_match():
    team_name = request.form['team_name']
    matches.delete_row(team_name)

    response = jsonify({
        'message': 'Match deleted successfully'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatePoints', methods=['POST'])
def update_points_route():
    request_payload = json.loads(request.form['data'])
    team_name = request_payload.get('team_name')
    wins = request_payload.get('wins')
    losses = request_payload.get('losses')
    point = request_payload.get('point')

    matches.update_points(team_name, wins, losses, point)

    response = jsonify({
        'message': 'Points updated successfully'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/viewPoints', methods=['GET'])
def view_points():
    try:
        cnx = get_sql_connection()
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM points"
        cursor.execute(query)

        points_data = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify(points_data)

    except mysql.connector.Error as err:
        print("Error viewing points table:", err)
        return jsonify({'error': 'Error viewing points table'})

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)