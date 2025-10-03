"""
Program name: sakila_assistant.py
Author: John Dosyal
Date last updated: 10/2/2025
Purpose: Program that allows a rental store clerk to interact with the Sakila video store database through a text-based menu. 
The program allows prepared statements and allow for data navigation with pagination
"""

# Import necessary libraries
from ast import Return
from math import e
import sqlite3

# Database Connection Function
def connect_db(db_name="Module 5/M05 Programming Assignment 2/sakila.db"):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print("Failed to connect to database:", e)
        print("Exiting program. \n")
        return None

# Pagination Helper Function
def paginate(data, per_page):
    for i in range(0, len(data), per_page):
        yield data[i:i + per_page]

# Database Interaction Functions

# View Customers
def get_customers(cursor):
    # Retrieves a basic list of all customers with their ID, first name, and last name.
    # The results are sorted by customer ID in ascending order.
    query = "SELECT customer_id, first_name, last_name FROM customer ORDER BY customer_id ASC"
    cursor.execute(query)
    return cursor.fetchall()

# View Customer Information
def get_customer_details(cursor, customer_id):
    # Retrieves detailed information about a specific customer using their customer_id.
    # The query joins four tables to get:
    # - First and last name from the 'customer' table
    # - Phone and address from the 'address' table (linked via address_id)
    # - City from the 'city' table (linked via city_id)
    # - Country from the 'country' table (linked via country_id)
    # - Email, active status, and last update from the 'customer' table
    query = """
    SELECT c.first_name, c.last_name, a.address, a.phone, ci.city, co.country, c.email, c.active, c.last_update 
    FROM customer AS c
    JOIN address AS a ON c.address_id = a.address_id
    JOIN city AS ci ON a.city_id = ci.city_id
    JOIN country AS co ON ci.country_id = co.country_id
    WHERE c.customer_id = ?
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchone()

# View Rental History for a Customer
def get_rentals_by_customer(cursor, customer_id):
    # Retrieves all rentals for a specific customer using their customer_id.
    # The query joins:
    # - 'rental' to 'inventory' (via inventory_id) to get the film info
    # - 'inventory' to 'film' (via film_id) to get the film title
    # - 'rental' to 'staff' (via staff_id) to get the staff member's full name
    # It returns:
    # - Rental ID, rental date, film title, return date, and staff name
    query = """
    SELECT r.rental_id, r.rental_date, f.title, r.return_date, s.first_name || ' ' || s.last_name AS staff_name
    FROM rental AS r
    JOIN inventory AS i ON r.inventory_id = i.inventory_id
    JOIN film AS f ON i.film_id = f.film_id
    JOIN staff AS s ON r.staff_id = s.staff_id
    WHERE r.customer_id = ?
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()

# View Available Films at a Store
def get_available_films_by_store(cursor, store_id):
    # Retrieves a list of available films at a specific store, avoiding duplicates using DISTINCT.
    # The query joins:
    # - 'film' to 'language' (via language_id) to get the language name
    # - 'film' to 'film_category' to get the category via 'category_id'
    # - 'film_category' to 'category' for the category name
    # - 'film' to 'inventory' to associate the film with a specific store
    # Filters the results by store_id
    # Returns: title, language, category, and rating of each film
    query = """
    SELECT DISTINCT f.title, l.name AS language, c.name AS category, f.rating AS rating
    FROM film AS f
    JOIN language AS l ON f.language_id = l.language_id
    JOIN film_category AS fc ON f.film_id = fc.film_id
    JOIN category AS c ON fc.category_id = c.category_id
    JOIN inventory AS i ON f.film_id = i.film_id
    WHERE i.store_id = ?
    """
    cursor.execute(query, (store_id,))
    return cursor.fetchall()

# Record a Payment for a Rental
def record_payment(cursor, customer_id, rental_id, amount, staff_id=1):
    # Inserts a new payment record into the 'payment' table.
    # Fields:
    # - customer_id: the ID of the customer making the payment (passed as a parameter)
    # - staff_id: the staff member processing the payment (passed as a parameter)
    # - rental_id: the rental associated with the payment (passed as a parameter)
    # - amount: the amount paid (passed as a parameter)
    # - payment_date: automatically set to the current timestamp using SQLite's datetime('now') function
    query = """
    INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES (?, ?, ?, ?, datetime('now'));
    """
    cursor.execute(query, (customer_id, staff_id, rental_id, amount))

# View Payment Information for a Customer
def get_payment_details(cursor, customer_id):
    # Retrieves detailed information about a specific customer using their customer_id.
    # The query joins four tables to get:
    # - First and last name from the 'customer' table
    # - Phone and address from the 'address' table (linked via address_id)
    # - City from the 'city' table (linked via city_id)
    # - Country from the 'country' table (linked via country_id)
    # - Email, active status, and last update from the 'customer' table
    query = """
    SELECT c.first_name, c.last_name, f.title, p.amount, p.payment_date, s.first_name || ' ' || s.last_name AS staff_name
    FROM customer AS c
    JOIN payment AS p ON c.customer_id = p.customer_id
    JOIN rental AS r ON p.rental_id = r.rental_id
    JOIN inventory AS i ON r.inventory_id = i.inventory_id
    JOIN film AS f ON i.film_id = f.film_id
    JOIN staff AS s ON p.staff_id = s.staff_id
    WHERE c.customer_id = ?
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()

# User Interface Functions

# View Customer Information
def view_customer_info(cursor):
    customers = get_customers(cursor)

# Prompt user to see if they know the customer ID
# If yes, prompt for ID and display details
    try:
        known_customer = input("Do you know the customer ID you would like to view? (y/n): ").strip().lower()

        if known_customer == 'y':
            try:
                cust_id = int(input("Enter customer ID: "))
                details = get_customer_details(cursor, cust_id)
                if details:
                    print(f"\nDetails for Customer ID {cust_id}:")
                    print(f"Name: {details[1]}, {details[0]}")
                    print(f"Phone: {details[2]}, Address: {details[3]}, City: {details[4]}, Country: {details[5]}")
                    print(f"Email: {details[6]}, Active: {'Yes' if details[7] else 'No'}, Last Update: {details[8]}")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Returning to main menu. \n")
                input("Press Enter to continue...")
                return
            
# If customer_id is not known, display paginated list of customers to choose from
        elif known_customer == 'n':
            page_size = int(input("How many customers per page? "))
            pages = list(paginate(customers, page_size))
            current = 0

            while True:
                print(f"\n--- Page {current + 1}/{len(pages)} ---\n")
                for i, cust in enumerate(pages[current], 1):
                    print(f"Entry # {i} | Customer ID: {cust[0]} | Name:{cust[2]} {cust[1]}")
                selection = input("\nSelect which entry you would like to view more information on. (Hit 0 for next page, -1 for previous page): \n")
                if selection == '0':
                    current = (current + 1) % len(pages)
                elif selection == '-1':
                    current = (current - 1) % len(pages)
                else:
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(pages[current]):
                            cust_id = pages[current][index][0]
                            details = get_customer_details(cursor, cust_id)
                            print(f"\nDetails for Customer ID {cust_id}:")
                            print(f"Name: {details[1]}, {details[0]}")
                            print(f"Phone: {details[2]}, Address: {details[3]}, City: {details[4]}, Country: {details[5]}")
                            print(f"Email: {details[6]}, Active: {'Yes' if details[7] else 'No'}, Last Update: {details[8]}")
                            input("Press Enter to continue...")
                            break

# If invalid selection, notify user and return to previous menu
                        else:
                            print("\nInvalid selection. \n")
                            print("Returning to previous menu. \n")
                            input("Press Enter to continue...")
                            break
                    except:
                        print("\nInvalid selection. \n")
                        print("Returning to previous menu. \n")
                        input("Press Enter to continue...")
                        break
        else:
            print("Invalid input. Returning to main menu. \n")
            input("Press Enter to continue...")
            return
    except:
        print("Invalid input. Returning to main menu. \n")
        input("Press Enter to continue...")
        return
    
# View Rental History for a Customer
# Similar structure to view_customer_info, but retrieves and displays rental history
def view_rentals(cursor):
    customers = get_customers(cursor)

# Prompt user to see if they know the customer ID
# If yes, prompt for ID and display rental history
    try:
        known_customer = input("Do you know the customer ID you would like to view? (y/n): ").strip().lower()

        if known_customer == 'y':
            try:
                cust_id = int(input("Enter customer ID: "))
                rentals = get_rentals_by_customer(cursor, cust_id)
                if rentals:
                    print(f"\nRentals for Customer ID {cust_id}:")
                    for r in rentals:
                        print(f"Rental ID: {r[0]} | Date Rented:{r[1]} | Film: {r[2]} | Return: {r[3]} | Staff: {r[4]}")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Returning to main menu. \n")
                input("Press Enter to continue...")
                return
            
# If customer_id is not known, display paginated list of customers to choose from
        elif known_customer == 'n':
            page_size = int(input("How many customers per page? "))
            pages = list(paginate(customers, page_size))
            current = 0

            while True:
                print(f"\n--- Page {current + 1}/{len(pages)} ---\n")
                for i, cust in enumerate(pages[current], 1):
                    print(f"Entry # {i} | Customer ID: {cust[0]} | Name:{cust[2]} {cust[1]}")
                selection = input("\nSelect which entry you would like to view more information on. (Hit 0 for next page, -1 for previous page): \n")
                if selection == '0':
                    current = (current + 1) % len(pages)
                elif selection == '-1':
                    current = (current - 1) % len(pages)
                else:
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(pages[current]):
                            cust_id = pages[current][index][0]
                            rentals = get_rentals_by_customer(cursor, cust_id)
                            print(f"\nRentals for Customer ID {cust_id}:")
                            for r in rentals:
                                print(f"Rental ID: {r[0]} | Date Rented:{r[1]} | Film: {r[2]} | Return: {r[3]} | Staff: {r[4]}")
                            input("Press Enter to continue...")
                            break

# If invalid selection, notify user and return to previous menu
                        else:
                            print("\nInvalid selection. \n")
                            print("Returning to previous menu. \n")
                            input("Press Enter to continue...")
                            break
                    except:
                        print("\nInvalid selection. \n")
                        print("Returning to previous menu. \n")
                        input("Press Enter to continue...")
                        break
        else:
            print("Invalid input. Returning to main menu. \n")
            input("Press Enter to continue...")
            return
    except:
        print("Invalid input. Returning to main menu. \n")
        input("Press Enter to continue...")
        return
    
# View Available Films at a Store
# Prompts user for store ID and displays available films at that store
def view_films(cursor):
    store_id = int(input("Enter store ID (1 or 2): "))
    films = get_available_films_by_store(cursor, store_id)
    for f in films:
        print(f"Title: {f[0]}, Language: {f[1]}, Category: {f[2]}, Rating: {f[3]}")
    input("Press Enter to continue...")

# Record a Payment for a Rental
# Prompts user for customer ID, rental ID, and payment amount, then records the payment
def add_payment(cursor):
    customer_id = int(input("Customer ID: "))
    rental_id = int(input("Rental ID: "))

# Check if customer ID exists
    try:
        cursor.execute("SELECT 1 FROM customer WHERE customer_id = ?", (customer_id,))
    except:
        print("Customer ID does not exist. \n")
        input("Press Enter to continue...")
        return

# Check if rental ID exists for the given customer
    rentals = get_rentals_by_customer(cursor, customer_id)
    rental_ids = [r[0] for r in rentals]
    if rental_id not in rental_ids:
        print("\nRental ID does not exist for this customer. \n")
        print("Returning to previous menu. \n")
        input("Press Enter to continue...")
        return

# Prompt for payment amount and record the payment
    amount = float(input("Payment Amount: "))
    record_payment(cursor, customer_id, rental_id, amount)
    print("Payment recorded. \n")
    input("Press Enter to continue...")

# View Payment Information for a Customer
# Similar structure to view_customer_info, but retrieves and displays payment information
def view_payment_info(cursor):
    customers = get_customers(cursor)

# Prompt user to see if they know the customer ID
# If yes, prompt for ID and display payment information
    try:
        known_customer = input("Do you know the customer ID you would like to view? (y/n): ").strip().lower()

        if known_customer == 'y':
            try:
                cust_id = int(input("Enter customer ID: "))
                payments = get_payment_details(cursor, cust_id)
                if payments:
                    print(f"\nPayments for Customer ID {cust_id}:")
                    for p in payments:
                        print(f"Customer: {p[0]} {p[1]} | Film: {p[2]} | Payment Amount: ${p[3]} | Payment Date: {p[4]} | Staff Member: {p[5]}")
                    input("Press Enter to continue...")
                    return
                else:
                    print("\nInvalid selection. \n")
                    print("Returning to previous menu. \n")
                    input("Press Enter to continue...")
                    return
            except ValueError:
                print("Invalid input. Returning to main menu. \n")
                input("Press Enter to continue...")
                return
            
# If customer_id is not known, display paginated list of customers to choose from
        elif known_customer == 'n':
            page_size = int(input("How many customers per page? "))
            pages = list(paginate(customers, page_size))
            current = 0

            while True:
                print(f"\n--- Page {current + 1}/{len(pages)} ---\n")
                for i, cust in enumerate(pages[current], 1):
                    print(f"{i}. {cust[0]} - {cust[2]} {cust[1]}")
                selection = input("\nSelect customer (0 for next, -1 for previous): \n")
                if selection == '0':
                    current = (current + 1) % len(pages)
                elif selection == '-1':
                    current = (current - 1) % len(pages)
                else:
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(pages[current]):
                            cust_id = pages[current][index][0]
                            payments = get_payment_details(cursor, cust_id)
                            print(f"\nPayments for Customer ID {cust_id}:")
                            for p in payments:
                                print(f"Customer: {p[0]} {p[1]} | Film: {p[2]} | Payment Amount: ${p[3]} | Payment Date: {p[4]} | Staff Member: {p[5]}")
                            input("Press Enter to continue...")
                            break

# If invalid selection, notify user and return to previous menu
                        else:
                            print("\nInvalid selection. \n")
                            print("Returning to previous menu. \n")
                            input("Press Enter to continue...")
                            break
                    except:
                        print("\nInvalid selection. \n")
                        print("Returning to previous menu. \n")
                        input("Press Enter to continue...")
                        break
        else:
            print("Invalid input. Returning to main menu. \n")
            input("Press Enter to continue...")
            return
    except:
        print("Invalid input. Returning to main menu. \n")
        input("Press Enter to continue...")
        return
    
# Main Program Function
def main():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

# Display menu and prompt for user choice
    while True:
        print("\n--- Sakila Video Store Assistant ---")
        print("1. View Customer Information")
        print("2. View Rental History for a Customer")
        print("3. View Available Films at a Store")
        print("4. Record a Payment for a Rental")
        print("5. View Payment Information for a Customer")
        print("6. Exit")
        choice = input("Enter choice: ")

# Execute the corresponding function based on user choice
        if choice == '1':
            view_customer_info(cursor)
        elif choice == '2':
            view_rentals(cursor)
        elif choice == '3':
            view_films(cursor)
        elif choice == '4':
            add_payment(cursor)
            conn.commit()
        elif choice == '5':
            view_payment_info(cursor)
        elif choice == '6':
            print("Goodbye! \n")
            input("Press Enter to continue...")
            break
        else:
            print("\nInvalid option. Try again. \n")
            input("Press Enter to continue...")

    conn.close()

# Run the main program
if __name__ == "__main__":
    main()

