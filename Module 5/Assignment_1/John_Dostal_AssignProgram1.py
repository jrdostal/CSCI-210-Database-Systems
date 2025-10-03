"""
Program name: John_Dostal_AssignProgram1.py
Author: John Dostal
Date last updated: 9/30/2025
Purpose: a python program with embedded SQL that opens a connection to the Chinook database. If the connection doesn't open successfully prints an error message from the database and ends the program. If connection opens successfully, prints a message stating the connection was successful. Uses a simple query to print the 'AlbumId, Title and ArtistId' albums in the database. After running the query, closes the database connection.
"""

import sqlite3 
from sqlite3 import Error

# Function to create a database connection
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("\n Connection successful. \n")
        return conn
    except Error as e:
        print(f"\n Error '{e}' occurred while connecting to the database. \n Exiting program.\n")
        return None

# Function to close the database connection
def close_connection(conn):
    if conn:
        conn.close()
        print("\n Connection closed. \n")
    else:
        print("\n No connection to close. \n")
    return

# Function to select all albums
def select_all_albums(conn):
    cur = conn.cursor()
    cur.execute("SELECT AlbumId, Title, ArtistId FROM albums")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return

# Optional: Function to print column names of the albums table
def print_column_names(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(albums);")
    column_names = [description[1] for description in cur.fetchall()]
    print("\n Column names in the albums table:")
    for name in column_names:
        print(name)
    return

# Main function to run the program
def main():
    database = r"Module 5/Assignment_1/chinook.db"
    # create a database connection
    connect = create_connection(database)
    if connect is None:
        print("\n Failed to create database connection. \n Exiting program.\n")
        return

    with connect:
        print("\n Querying all albums: \n")
        select_all_albums(connect)
        # print_column_names(connect) # Uncomment this line to print column names

    close_connection(connect)

# Run the main function if this script is executed directly
if __name__ == '__main__':
    main()
else:
    print("\n This program is not being run directly. \n Exiting program.\n")