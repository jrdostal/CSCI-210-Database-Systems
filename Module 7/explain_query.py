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
    SELECT f.title, f.description, l.name
    FROM film AS f
    JOIN language AS l ON f.language_id = l.language_id
    LIMIT 300;
    """)
    return sql_query

def query_2(sql_query):
    sql_query = str("""
    SELECT DISTINCT r.customer_id
    FROM rental AS r
    JOIN inventory AS i ON r.inventory_id = i.inventory_id
    JOIN film AS f ON i.film_id = f.film_id
    WHERE f.title = 'MONTEZUMA COMMAND';
    """)
    return sql_query

def query_3(sql_query):
    sql_query = str("""
    SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_amount
    FROM customer AS c
    JOIN payment AS p ON c.customer_id = p.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name;
    """)
    return sql_query

def query_4(sql_query):
    sql_query = str("""
    SELECT DISTINCT a.actor_id, a.first_name, a.last_name
    FROM actor AS a
    JOIN film_actor AS fa ON a.actor_id = fa.actor_id
    JOIN film AS f ON fa.film_id = f.film_id
    WHERE f.rental_rate = 0.99;
    """)
    return sql_query

def query_5(sql_query):
    sql_query = str("""
    SELECT DISTINCT c.first_name, c.last_name, a.address, ci.city, co.country, a.postal_code, a.phone
    FROM customer AS c
    JOIN address AS a ON c.address_id = a.address_id
    JOIN city AS ci ON a.city_id = ci.city_id
    JOIN country AS co ON ci.country_id = co.country_id
    JOIN rental AS r ON c.customer_id = r.customer_id
    WHERE r.return_date IS NULL;
    """)
    return sql_query

def create_indexes(cursor):

    # Connect to the database
    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()

    # Create indexes to optimize query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_film_language_id ON film(language_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_language_language_id ON language(language_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_film_title ON film(title);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_film_id ON inventory(film_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rental_inventory_id ON rental(inventory_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_payment_customer_id ON payment(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_film_rental_rate ON film(rental_rate);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_film_actor_film_id ON film_actor(film_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_film_actor_actor_id ON film_actor(actor_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rental_customer_id ON rental(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rental_return_date ON rental(return_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_address_address_id ON address(address_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_city_city_id ON city(city_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_country_country_id ON country(country_id);")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Notify the user that indexes have been created
    print("Indexes created successfully.")

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

    create_indexes(None)
    main()
    print("\n All query explanations have been displayed.")
    print("Exiting program. \n")
    input("Press Enter to continue...")
