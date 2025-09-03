# Program name: JohnDostalStudyMor.py
# Author: John Dostal
# Date last updated: 9/3/2025
# Purpose: Run menu program that stores data in two separate files. One file is for participant data and the other is for survey data.

import os
from datetime import datetime

PARTICIPANT_FILE = "participant.dat"
SURVEY_FILE = "survey.dat"

def add_participant():
    print("\n--- Add New Participant ---")
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()
    age = input("Enter Age: ").strip()
    gender = input("Enter Gender: ").strip()

    try:
        with open(PARTICIPANT_FILE, "r") as file:
            lines = file.readlines()
            participant_id = len(lines) + 1
    except FileNotFoundError:
        participant_id = 1

    treatment = "StudyMor" if participant_id % 2 == 0 else "Placebo"

    with open(PARTICIPANT_FILE, "a") as file:
        record = f"{participant_id},{first_name},{last_name},{age},{gender},{treatment}\n"
        file.write(record)

    print(f"Participant added with ID {participant_id} and Treatment: {treatment}")

def display_participants():
    print("\n--- List of Participants ---")
    if not os.path.exists(PARTICIPANT_FILE):
        print("No participant records found.")
        return

    with open(PARTICIPANT_FILE, "r") as file:
        lines = file.readlines()
        if not lines:
            print("No participants found.")
            return

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 6:
                pid, fname, lname, age, gender, treatment = parts
                print(f"ID: {pid}, Name: {fname} {lname}, Age: {age}, Gender: {gender}, Treatment: {treatment}")
            else:
                print("Malformed record:", line.strip())

def collect_survey():
    print("\n--- Collect Survey ---")
    display_participants()
    participant_id = input("\nEnter Participant ID for survey: ").strip()

    print("\nPlease answer the following (yes/no):")
    headache = input("Did you have headaches? ").strip().lower()
    constipation = input("Did you have constipation? ").strip().lower()
    sleep_issue = input("Did you have difficulty sleeping? ").strip().lower()
    other_effects = input("List any other side effects (or 'none'): ").strip()
    study_more = input("Did you feel like you could study more? ").strip().lower()

    date = datetime.now().strftime("%Y-%m-%d")

    with open(SURVEY_FILE, "a") as file:
        record = f"{date},{participant_id},{headache},{constipation},{sleep_issue},{other_effects},{study_more}\n"
        file.write(record)

    print("Survey recorded successfully.")

def main():
    while True:
        print("\n=== Aurora Voyagers Clinical Study Menu ===")
        print("1. Add New Participant")
        print("2. Collect Survey for Participant")
        print("3. Display Participants")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ").strip()

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

