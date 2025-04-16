import mysql.connector
from sql_connection import get_sql_connection

def insert_row(team_name, team_id, wins, losses, point):
    try:
        cnx = get_sql_connection()
        cursor = cnx.cursor()

        # Insert a row into the table
        query = "INSERT INTO points (team_name, team_id, wins, losses, point) VALUES (%s, %s, %s, %s, %s)"
        data = (team_name, team_id, wins, losses, point)
        cursor.execute(query, data)

        cnx.commit()
        print("Row inserted successfully")

    except mysql.connector.Error as err:
        print("Error inserting row:", err)

    finally:
        cursor.close()

def delete_row(team_name):
    try:
        cnx = get_sql_connection()
        cursor = cnx.cursor()

        # Delete a row from the table based on team_name
        query = "DELETE FROM points WHERE team_name = %s"
        data = (team_name,)
        cursor.execute(query, data)

        cnx.commit()
        print("Row deleted successfully")

    except mysql.connector.Error as err:
        print("Error deleting row:", err)

    finally:
        cursor.close()

def update_points(team_name, wins, losses, point):
    try:
        cnx = get_sql_connection()
        cursor = cnx.cursor()

        # Update the row in the table
        query = "UPDATE points SET wins = %s, losses = %s, point = %s WHERE team_name = %s"
        data = (wins, losses, point, team_name)
        cursor.execute(query, data)

        cnx.commit()
        print("Row updated successfully")

    except mysql.connector.Error as err:
        print("Error updating row:", err)

    finally:
        cursor.close()




# Example usage:
# Make a GET request to /viewPoints endpoint to view the points table


# Example usage:
# Inserting a row
#insert_row('Mumbai Indians', 1, 100, 50, 200)

# Deleting a row
#delete_row('Mumbai Indians')
