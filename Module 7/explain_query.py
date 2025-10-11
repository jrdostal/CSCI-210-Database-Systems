"""
Program name: explain_query.py
Author: John Dostal
Date last updated: 10/11/2025
Purpose: Program to demonstrate the use of EXPLAIN QUERY PLAN in SQLite.
"""

# Import the sqlite3 module
import sqlite3
import time


# functions to create the SQL queries to be explained/run
def query_1(sql_query):
    sql_query = str("""
    SELECT title, description, name
    FROM film 
    JOIN language ON film.language_id = language.language_id 
    LIMIT 300;
    """)
    return sql_query

def query_2(sql_query):
    sql_query = str("""
    SELECT customer_id 
    FROM rental 
    JOIN inventory ON rental.inventory_id = inventory.inventory_id
    JOIN film ON inventory.film_id = film.film_id
    WHERE film.title = 'MONTEZUMA COMMAND';
    """)
    return sql_query

def query_3(sql_query):
    sql_query = str("""
    SELECT first_name, last_name, sum(amount)
    FROM customer 
    JOIN payment ON customer.customer_id = payment.customer_id
    GROUP BY customer.customer_id, first_name, last_name;
    """)
    return sql_query

def query_4(sql_query):
    sql_query = str("""
    SELECT distinct actor.*
    FROM actor 
    JOIN film_actor ON actor.actor_id = film_actor.actor_id
    JOIN film ON film_actor.film_id = film.film_id
    WHERE film.rental_rate = .99;
    """)
    return sql_query

def query_5(sql_query):
    sql_query = str("""
    SELECT first_name, last_name, address, city, country, postal_code, phone 
    FROM customer 
    JOIN address ON customer.address_id = address.address_id 
    JOIN city ON address.city_id = city.city_id 
    JOIN country ON city.country_id = country.country_id 
    WHERE customer_id IN (SELECT customer_id FROM rental WHERE return_date IS NULL);
    """)
    return sql_query

# function to connect to the SQLite database
def connect_to_database(db_name = "Module 7/sakila-1.db"):

    # Attempt to connect to the SQLite database
    # If connection fails, print an error message and exit the program
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
            print("Failed to connect to database:", e)
            print("Exiting program. \n")
            return None

# Function to view query explanations
# Also measures and prints the execution time of the EXPLAIN QUERY PLAN command
def view_query(cursor, sql_query):

    # Start the timer
    start_time = time.perf_counter_ns()
    
    # Prepend EXPLAIN QUERY PLAN to the SQL query
    sql_query = "EXPLAIN QUERY PLAN " + str(sql_query)
    cursor.execute(sql_query)
    plan_rows = cursor.fetchall()

    # End the timer
    end_time = time.perf_counter_ns()

    # Calculate execution time in nanoseconds
    execution_time = end_time - start_time

    # Initialize a counter for indentation
    counter = 0

    # Print each row of the query plan with indentation
    print("Query Plan:")
    for row in plan_rows:
        node_id, parent_id, unused, detail = row
        indent = "  " * counter
        print(f"{indent}ID: {node_id}, Parent: {parent_id}, Detail: {detail}")
        counter += 1
    print(f"\nExecution Time: {execution_time} nanoseconds")
    input("Press Enter to continue...")

# Main function to run the program
def main():

    # Connect to the database
    conn = connect_to_database()
    if conn is None:
        return

    # Create a cursor object
    cursor = conn.cursor()

    # Set PRAGMA to automatically explain queries
    cursor.execute("PRAGMA eqp = OFF;")

    # List of queries to explain
    queries = [query_1(cursor), query_2(cursor), query_3(cursor), query_4(cursor), query_5(cursor)]

    # Loop through each query and display its explanation
    for i, sql_query in enumerate(queries, start=1):
        print(f"\nExplanation for Query {i}:")
        view_query(cursor, sql_query)

    # Close the database connection
    conn.close()

# Run the main function
if __name__ == "__main__":
    main()
    print("\n All query explanations have been displayed.")
    print("Exiting program. \n")
    input("Press Enter to continue...")
