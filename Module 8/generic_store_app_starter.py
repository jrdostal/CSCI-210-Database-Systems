"""
Program name: generic_store_app_starter.py
Author: John Dostal
Date last updated: 10/14/2025
Purpose: Starter code for a generic store application using SQLite.
         Students will complete the SQL operations to manage customers,
         products, and purchases.
"""

import sqlite3
from datetime import datetime

DB_PATH = 'your_database_file.db'  # <-- students should update this

def register_customer():
    print("=== Register New Customer ===")
    # TODO: Add SQL code to insert into CUSTOMER and ADDRESS tables

def view_all_customers():
    print("=== All Registered Customers ===")
    # TODO: Add SQL code to SELECT and display joined CUSTOMER + ADDRESS data

def update_customer():
    print("=== Update Customer Info ===")
    # TODO: Add SQL code to update CUSTOMER and ADDRESS records

def view_products():
    print("=== Available Products ===")
    # TODO: Add SQL code to SELECT and display PRODUCT table contents

def purchase_product():
    print("=== Purchase Product ===")
    # TODO:
    # - Validate inventory
    # - Create INVOICE and LINE items
    # - Update PRODUCT quantities
    # - Log payment in ACCOUNT_TRANSACTION and PAYMENT_DETAIL if card used

def main():
    while True:
        print("\\n=== Generic Store Menu ===")
        print("1. Register New Customer")
        print("2. View Products")
        print("3. Purchase Product")
        print("4. View All Customers")
        print("5. Update Customer Info")
        print("6. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            register_customer()
        elif choice == '2':
            view_products()
        elif choice == '3':
            purchase_product()
        elif choice == '4':
            view_all_customers()
        elif choice == '5':
            update_customer()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()

