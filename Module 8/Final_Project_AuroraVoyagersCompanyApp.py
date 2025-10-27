"""
Program name: Final_Project_AuroraVoyagersCompanyApp.py
Author: John Dostal
Date last updated: 10/16/2025
Purpose: This program is a command-line application for managing customers and spaceship orders for Aurora Voyagers Company.
It allows users to register new customers, view available spaceships, order spaceships, view and update customer information.
"""

# Import necessary libraries
import datetime
import sqlite3

# Database Connection Function
# Note: Ensure the database file path is correct, as I had to change the path to run it on my machine.
def connect_db(db_name='Module 8/AuroraVoyagersCompany.db'):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print("Failed to connect to database:", e)
        print("Exiting program. \n")
        return None

# Database Close Function
def close_db(connection):
    if connection:
        connection.close()

# Pagination Helper Function
def paginate(data, per_page):
    for i in range(0, len(data), per_page):
        yield data[i:i + per_page]


# Get Table Columns Helper Function
def get_Table_Columns(table_name):
    connection = connect_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [info[1] for info in cursor.fetchall()]
    close_db(connection)
    return columns

# Register New Customer
def register_customer(cursor, connection):
    print("=== Register New Customer ===")
    if connection is None:
        return
    Customer_Columns = get_Table_Columns("Customer")
    customer_values = []
    for col in Customer_Columns:
        col_value = input(f"Enter {col}: ").strip()
        customer_values.append(col_value)
    cursor.execute("INSERT INTO Customer VALUES (" + ", ".join(["?"] * len(customer_values)) + ")", customer_values)
    connection.commit()

# Get List of all Spaceships
def get_spaceships(cursor):
    query = "SELECT SpaceshipID, Make, Model, ShipName, SerialNumber, ModelYear, Condition, Modifications, SalePrice, LastMaintenanceDate, Available FROM Spaceship WHERE Available != 0"
    cursor.execute(query)
    return cursor.fetchall()

# Get Spaceship Details by ID
def get_spaceship_details(cursor, spaceship_id):
    query = "SELECT * FROM Spaceship WHERE SpaceshipID = ?"
    cursor.execute(query, (spaceship_id,))
    return cursor.fetchone()


# Get List of all Customers
def get_customers(cursor):
    query = "SELECT CustomerID, CustomerLastName, CustomerFirstName FROM Customer"
    cursor.execute(query)
    return cursor.fetchall()

# Get Customer Details by ID
def get_customer_details(cursor, customer_id):
    query = "SELECT * FROM Customer WHERE CustomerID = ?"
    cursor.execute(query, (customer_id,))
    return cursor.fetchone()

# View Customer Information
def view_customer_info(cursor):
    cursor = cursor
    customers = get_customers(cursor)

# Prompt user to see if they know the customer ID
# If yes, prompt for ID and display details
    try:
        known_customer = input("Do you know the customer ID you would like to view? (y/n): ").strip().lower()

        if known_customer == 'y':
            try:
                cust_id = int(input("Enter customer ID: ").strip())
                details = get_customer_details(cursor, cust_id)
                if details:
                    print(f"\nDetails for Customer ID {cust_id}:")
                    print(f"Name: {details[2]}, {details[1]}")
                    print(f"Company Name: {details[3]}")
                    print(f"Phone: {details[4]}, Address: {details[6]}")
                    print(f"Email: {details[5]}, Date of Birth: {details[7]}, Identity Verified: {details[8]}")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Returning to main menu. \n")
                input("Press Enter to continue...").strip()
                return
            
# If customer_id is not known, display paginated list of customers to choose from
        elif known_customer == 'n':
            page_size = int(input("How many customers per page? ").strip())
            pages = list(paginate(customers, page_size))
            current = 0

            # Loop to navigate pages and select customer
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
                            print(f"Name: {details[2]}, {details[1]}")
                            print(f"Company Name: {details[3]}")
                            print(f"Phone: {details[4]}, Address: {details[6]}")
                            print(f"Email: {details[5]}, Date of Birth: {details[7]}, Identity Verified: {details[8]}")
                            input("Press Enter to continue...")
                            break

# If invalid selection, notify user and return to previous menu
                        else:
                            print("\nInvalid selection 1. \n")
                            print("Returning to previous menu. \n")
                            input("Press Enter to continue...")
                            break
                    except Exception as e:
                        print("\nInvalid selection 2. \n", e)
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
    
# Update Customer Information
def update_customer():
    print("=== Update Customer Info ===")
    CustomerID = input("Enter Customer ID to update: ").strip()
    Customer_Columns = get_Table_Columns("Customer")
    print("Available columns to update:", Customer_Columns)
    column_to_update = input("Enter the column to update: ").strip()
    new_value = input("Enter the new value: ").strip()
    connection = connect_db()
    if not connection:
        return
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Customer SET {column_to_update} = ? WHERE CustomerID = ?", (new_value, CustomerID))
    connection.commit()

# View Available Spaceships
def view_spaceships(cursor, connection):
    print("=== Available Spaceships ===")
    if connection is None:
        return
    Spaceships = get_spaceships(cursor)
    for spaceship in Spaceships:
        details = get_spaceship_details(cursor, spaceship[0])
        print(f"\nDetails for Spaceship ID {spaceship[0]}:")
        print(f"Make: {details[4]}, Model: {details[5]}, Ship Name: {details[6]}, Serial Number:  {details[1]}")
        print(f"Model Year: {details[7]}, Condition:  {details[8]}, Last Maintenance Date: {details[11]}")
        print(f"Modifications: {details[9]}, Sale Price: {details[10]}, Stock Available:  {details[12]}, ")
        input("Press Enter to continue...")

# Select Spaceship Helper Function
def select_Spaceship(cursor, connection):

    # Prompt user to see if they know the customer ID
    # If yes, prompt for ID and display details
    try:
        known_spaceship = input("Do you know the spaceship ID you would like to view? (y/n): ").strip().lower()

        if known_spaceship == 'y':
            try:
                spaceship_id = int(input("Enter spaceship ID: ").strip())
                details = get_spaceship_details(cursor, spaceship_id)
                if details:
                    print(f"\nDetails for Spaceship ID {spaceship_id}:")
                    print(f"Make: {details[1]}, Model: {details[2]}, Ship Name: {details[3]}, Serial Number:  {details[4]}")
                    print(f"Model Year: {details[5]}, Condition:  {details[6]}, Last Maintenance Date: {details[9]}")
                    print(f"Modifications: {details[7]}, Sale Price: {details[8]}, Stock Available:  {details[10]}, ")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Returning to main menu. \n")
                input("Press Enter to continue...").strip()
                return
            
        elif known_spaceship == 'n':
            # Display available spaceships
            view_spaceships(cursor, connection)

        else:
            print("Invalid input. Returning to main menu. \n")
            input("Press Enter to continue...").strip()
            return
    except:
        print("Invalid input. Returning to main menu. \n")
        input("Press Enter to continue...").strip()
        return

    # Prompt user to select spaceship
    # Checks if input is valid
    while True:
        try:
            SpaceshipID = int(input("Enter the Spaceship ID to purchase: "))
            cursor.execute("SELECT * FROM Spaceship WHERE SpaceshipID = ?", (SpaceshipID,))
            selected_spaceship = cursor.fetchone()
            if selected_spaceship is None:
                print("Invalid Spaceship ID.")
                print("Please choose another spaceship.")
            else:
                return SpaceshipID
        except ValueError:
            print("Invalid input. Please enter a valid integer for Spaceship ID.")

# Order Spaceship Function
def order_spaceship(cursor, connection):
    print("=== Purchase Spaceship ===")
    if connection is None:
        return
    else:
        
        # Loop to validate Customer ID
        while True:
            CustomerID = input("Enter your Customer ID: ").strip()
            cursor.execute("SELECT * FROM Customer WHERE CustomerID = ?", (CustomerID,))
            customer = cursor.fetchone()
            if customer is None:
                print("Invalid Customer ID.")
                print("Please register as a new customer if you don't have an ID.")
            else: 
                break

        #Run function to list and select a spaceship for purchase
        SpaceshipID = select_Spaceship(cursor, connection)
        if SpaceshipID is None:
            return
        
        # Check spaceship availability
        Spaceship_quantity = cursor.execute("SELECT Available FROM Spaceship WHERE SpaceshipID = ?", (SpaceshipID,)).fetchone()[0]
        if Spaceship_quantity > 0:
            cursor.execute("UPDATE Spaceship SET Available = 0 WHERE SpaceshipID = ?", (SpaceshipID,))
        else:
            print("Sorry, this spaceship is not available.")
            print("Please choose another spaceship.")
        
        # Confirm purchase loop
        Continue = True
        while Continue == True:
            confirm = input(f"Confirm purchase of Spaceship ID {SpaceshipID} (yes/no): ").strip().lower()
            if confirm in ['yes', 'no']:
                if confirm == 'no':
                    print("Purchase cancelled.")
                    Continue = False
                    break
                elif confirm == 'yes':

                    # Get user input for order details
                    # Creates new Order for transaction
                    Destination = input("Enter the destination for delivery: ")
                    OrderStatus = "Processing"
                    DiscountApplied = 0
                    SalePrice = cursor.execute("SELECT SalePrice FROM Spaceship WHERE SpaceshipID = ?", (SpaceshipID,)).fetchone()[0]
                    TaxRate = 1.1  # Assuming a fixed tax rate of 10%
                    OrderTotal = (SalePrice - DiscountApplied) * TaxRate
                    OrderDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    HighestOrderID = cursor.execute("SELECT MAX(OrderID) FROM Orders").fetchone()[0]
                    if HighestOrderID is None:
                        NewOrderID = 1
                    else:
                        NewOrderID = HighestOrderID + 1
                    cursor.execute("""INSERT INTO Orders (OrderID, InvoiceID, CustomerID, SpaceshipID, OrderDateTime, Destination,
                                        OrderStatus, DiscountApplied, OrderTotal)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (NewOrderID, "Null", CustomerID, SpaceshipID, OrderDateTime, Destination,
                                    OrderStatus, DiscountApplied, OrderTotal))
                    # Commit transaction and close connection
                    connection.commit()
                    print("Purchase successful!")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        return

# Main Program Function
def main():
    # Display menu and prompt for user choice using loop
    while True:
        print("\n=== Generic Store Menu ===")
        print("1. Register New Customer")
        print("2. View Spaceships")
        print("3. Order Spaceship")
        print("4. View Customer Info")
        print("5. Update Customer Info")
        print("6. Exit")
        choice = input("Select an option: ")

        # Execute the corresponding function based on user choice
        if choice == '1':
            connection = connect_db()
            if not connection:
                return
            cursor = connection.cursor()
            register_customer(cursor, connection)
            close_db(connection)
        elif choice == '2':
            connection = connect_db()
            if not connection:
                return
            cursor = connection.cursor()
            view_spaceships(cursor, connection)
            close_db(connection)
        elif choice == '3':
            connection = connect_db()
            if not connection:
                return
            cursor = connection.cursor()
            order_spaceship(cursor, connection)
            close_db(connection)
        elif choice == '4':
            connection = connect_db()
            if not connection:
                return
            cursor = connection.cursor()
            view_customer_info(cursor)
            close_db(connection)
        elif choice == '5':
            connection = connect_db()
            if not connection:
                return
            cursor = connection.cursor()
            update_customer()
            close_db(connection)
        elif choice == '6':
            print("Goodbye! \n")
            input("Press Enter to continue...")
            break
        else:
            print("\nInvalid option. Try again. \n")
            input("Press Enter to continue...")

# Run the main function
if __name__ == '__main__':
    main()

