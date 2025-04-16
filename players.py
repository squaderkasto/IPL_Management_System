from datetime import datetime
from sql_connection import get_sql_connection

def insert_player(connection, player):
    cursor = connection.cursor()

    player_query = ("INSERT INTO players "
                    "(team_id, player_id, player_name, player_age)"
                    "VALUES (%s, %s, %s, %s)")
    player_data = (player['team_id'], player['player_id'], player['player_name'], player['player_age'])

    cursor.execute(player_query, player_data)
    player_id = cursor.lastrowid

    player_details_query = ("INSERT INTO player_detail "
                            "(team_id, player_id, total_run, total_wicket, price)"
                            "VALUES (%s, %s, %s, %s, %s)")

    for player_detail_record in player['player_detail']:
        player_detail_data = (player['team_id'], player['player_id'],
                              player_detail_record['total_run'], player_detail_record['total_wicket'],
                              player_detail_record['price'])
        cursor.execute(player_details_query, player_detail_data)

    connection.commit()

    return player_id



def get_player_details(connection, player_id):
    cursor = connection.cursor()

    query = "SELECT * from player_detail where player_id = %s"

   # query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
    #        "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
    #        "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (player_id, )

    cursor.execute(query, data)

    records = []
    for (team_id, player_id, total_run, total_wicket, price) in cursor:
        records.append({
            'team_id': team_id,
            'player_id': player_id,
            'total_run': total_run,
            'total_wicket': total_wicket,
            'price': price
        })

    cursor.close()

    return records

def get_all_players(connection):
    cursor = connection.cursor()
    query = ("SELECT p.team_id, p.player_id, p.player_name, p.player_age, t.team_name "
             "FROM players p "
             "JOIN team t ON p.team_id = t.team_id")
    cursor.execute(query)
    response = []
    for (team_id, player_id, player_name, player_age, team_name) in cursor:
        response.append({
            'team_id': team_id,
            'player_id': player_id,
            'player_name': player_name,
            'player_age': player_age,
            'team_name': team_name  # Include team name in the response
        })

    cursor.close()

    # append player details in each player
    for record in response:
        record['player_details'] = get_player_details(connection, record['player_id'])

    return response


if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_players(connection))
    #print(get_player_details(connection,4))
    '''print(insert_player(connection, {
         'team_id': 4,
         'player_id': 101,
         'player_name':'Dhoni',
         'player_age':42,
         'player_detail': [
             {
                 'team_id': 4,
                 'player_id': 102,
                 'total_run': 10504,
                 'total_wicket':10,
                 'price':25.5
             },
         ]
     }))'''