# Program name: JohnDostalStudyMor.py
# Author: John Dostal
# Date last updated: 9/3/2025
# Purpose: Run menu program that stores data in two separate files. One file is for participant data and the other is for survey data.

# Import necessary modules
import os
from datetime import datetime

# Constants for file names
PARTICIPANT_FILE = "participant.dat"
SURVEY_FILE = "survey.dat"

# Function to add a new participant
def add_participant():  

    # Input to add new participant
    print("\n--- Add New Participant ---")
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()
    age = input("Enter Age: ").strip()
    gender = input("Enter Gender: ").strip()

    # Error handling for participant data
    try:
        with open(PARTICIPANT_FILE, "r") as file:
            lines = file.readlines()
            participant_id = len(lines) + 1
    except FileNotFoundError:
        participant_id = 1

    # Assign treatment based on participant ID (even: StudyMor, odd: Placebo)
    treatment = "StudyMor" if participant_id % 2 == 0 else "Placebo"

    # Write participant data to file
    with open(PARTICIPANT_FILE, "a") as file:
        record = f"{participant_id},{first_name},{last_name},{age},{gender},{treatment}\n"
        file.write(record)

    print(f"Participant added with ID {participant_id} and Treatment: {treatment}")

# Function to display all participants
def display_participants():
    print("\n--- List of Participants ---")

    # Error handling for lack of participants file
    if not os.path.exists(PARTICIPANT_FILE):
        print("No participant records found.")
        return

    # Read participant data from file
    with open(PARTICIPANT_FILE, "r") as file:
        lines = file.readlines()

        # Error handling for lack of participants in participants file
        if not lines:
            print("No participants found.")
            return

        # Loop to display participants that exist in participants file
        for line in lines:
            parts = line.strip().split(",")

            # Error handling for malformed participant records
            if len(parts) == 6:
                pid, fname, lname, age, gender, treatment = parts
                print(f"ID: {pid}, Name: {fname} {lname}, Age: {age}, Gender: {gender}, Treatment: {treatment}")
            else:
                print("Malformed record:", line.strip())

# Function to collect survey data
def collect_survey():

    # Input to collect survey data
    print("\n--- Collect Survey ---")
    display_participants()
    participant_id = input("\nEnter Participant ID for survey: ").strip()

    # Error handling for invalid participant ID
    if not participant_id.isdigit():
        print("Invalid Participant ID. Please enter a numeric ID. Returning to main menu.")
        return
    else:
        participant_id = int(participant_id)

    # Continued input to collect survey data. Also contains error handling for yes/no input.
    print("\nPlease answer the following (yes/no):")

    headache_loop = True
    constipation_loop = True
    sleep_issue_loop = True
    study_more_loop = True

    # Loop to collect input for survey data
    while headache_loop:
        headache_1 = input("Did you have headaches? ").strip().lower()
        if headache_1 not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            headache_loop = False
            headache = headache_1

    # Loop to collect input for survey data
    while constipation_loop:
        constipation_1 = input("Did you have constipation? ").strip().lower()
        if constipation_1 not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            constipation_loop = False
            constipation = constipation_1

    # Loop to collect input for survey data
    while sleep_issue_loop:
        sleep_issue_1 = input("Did you have difficulty sleeping? ").strip().lower()
        if sleep_issue_1 not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            sleep_issue_loop = False
            sleep_issue = sleep_issue_1


    other_effects = input("List any other side effects (or 'none'): ").strip()

    # Loop to collect input for survey data
    while study_more_loop:
        study_more_1 = input("Did you feel like you could study more? ").strip().lower()
        if study_more_1 not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            study_more_loop = False
            study_more = study_more_1

    date = datetime.now().strftime("%Y-%m-%d")

    # Code to append survey file with survey data for participant
    with open(SURVEY_FILE, "a") as file:
        record = f"{date},{participant_id},{headache},{constipation},{sleep_issue},{other_effects},{study_more}\n"
        file.write(record)

    print("Survey recorded successfully.")

# Function to run the main menu
def main():

    # Main menu loop
    menu_loop = True

    while menu_loop:
        print("\n=== Aurora Voyagers Clinical Study Menu ===")
        print("1. Add New Participant")
        print("2. Collect Survey for Participant")
        print("3. Display Participants")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ").strip()

        # Menu options handling
        if choice == "1":
            add_participant()
        elif choice == "2":
            collect_survey()
        elif choice == "3":
            display_participants()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

