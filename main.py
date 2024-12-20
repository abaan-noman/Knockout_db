import sqlite3
import os

DB_FILE = "knockout_db.db"
SCHEMA_FILE = "knockout_db.sql"

# Initialize database from schema
def initialize_database():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn, open(SCHEMA_FILE, 'r') as schema_file:
            schema = schema_file.read()
            conn.executescript(schema)
        print(f"Database initialized from {SCHEMA_FILE} and saved to {DB_FILE}.")

# Display tables in a formatted way
def display_table(headers, rows):
    header_line = " | ".join(f"{col:^20}" for col in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(f"{str(cell):^20}" for cell in row))

# Add a fighter
def add_fighter():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        name = input("Enter fighter name: ")
        weight_class = input("Enter weight class: ")
        nationality = input("Enter nationality: ")
        cursor.execute("INSERT INTO Fighter (name, weight_class, nationality) VALUES (?, ?, ?);", 
                       (name, weight_class, nationality))
        conn.commit()
        print("Fighter added successfully.")

# Add an event
def add_event():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        name = input("Enter event name: ")
        date = input("Enter event date (YYYY-MM-DD): ")
        location = input("Enter event location: ")
        cursor.execute("INSERT INTO Event (name, date, location) VALUES (?, ?, ?);", 
                       (name, date, location))
        conn.commit()
        print("Event added successfully.")

# Add a fight
def add_fight():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        event_id = input("Enter event ID: ")
        fighter_one_id = input("Enter Fighter 1 ID: ")
        fighter_two_id = input("Enter Fighter 2 ID: ")
        rounds = input("Enter number of rounds: ")
        outcome = input("Enter outcome: ")
        method_of_victory = input("Enter method of victory: ")
        cursor.execute("""INSERT INTO Fight 
                          (event_id, fighter_one_id, fighter_two_id, rounds, outcome, method_of_victory) 
                          VALUES (?, ?, ?, ?, ?, ?);""",
                       (event_id, fighter_one_id, fighter_two_id, rounds, outcome, method_of_victory))
        conn.commit()
        print("Fight added successfully.")

# Add participation (Fighters_events)
def add_participation():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        fighter_id = input("Enter Fighter ID: ")
        event_id = input("Enter Event ID: ")
        result = input("Enter result (Win/Loss/Draw): ")
        round_num = input("Enter the round number: ")
        cursor.execute("""INSERT INTO Fighters_events (fighter_id, event_id, result, round) 
                          VALUES (?, ?, ?, ?);""",
                       (fighter_id, event_id, result, round_num))
        conn.commit()
        print("Participation record added successfully.")

# Add a statistic
def add_statistic():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Enter Fighter ID and Statistic Name
        fighter_id = input("Enter Fighter ID: ")
        statistic_name = input("Enter Statistic Name (e.g., 'Strike Accuracy'): ")
        
        # Check if the statistic name exists in the Statistics table
        cursor.execute("SELECT statistic_id FROM Statistics WHERE name = ?;", (statistic_name,))
        statistic = cursor.fetchone()
        
        # If the statistic name does not exist, insert it into the Statistics table
        if statistic:
            statistic_id = statistic[0]
        else:
            cursor.execute("INSERT INTO Statistics (name) VALUES (?);", (statistic_name,))
            conn.commit()  # Commit the insertion of the new statistic name
            
            # Fetch the statistic_id of the newly added statistic
            cursor.execute("SELECT statistic_id FROM Statistics WHERE name = ?;", (statistic_name,))
            statistic_id = cursor.fetchone()[0]
            print(f"Statistic '{statistic_name}' added successfully.")
        
        # Enter the statistic value
        statistic_value = input(f"Enter {statistic_name} value: ")
        
        # Insert the statistic for the given fighter
        cursor.execute("""INSERT INTO Fighter_statistics (fighter_id, statistic_id, statistic_value)
                          VALUES (?, ?, ?);""", (fighter_id, statistic_id, statistic_value))
        
        conn.commit()


# Query and display all fighters
def query_all_fighters():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fighter;")
        fighters = cursor.fetchall()
        if fighters:
            headers = ["ID", "Name", "Weight Class", "Nationality"]
            display_table(headers, fighters)
        else:
            print("No fighters found.")

# Query all events
def query_all_events():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Event;")
        events = cursor.fetchall()
        if events:
            headers = ["ID", "Name", "Date", "Location"]
            display_table(headers, events)
        else:
            print("No events found.")

# Query fights in an event
def query_fights_in_event():
    query_all_events()
    event_id = input("Enter the Event ID to view fights: ")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Fight WHERE event_id = ?;""", (event_id,))
        fights = cursor.fetchall()
        if fights:
            headers = ["Fight ID", "Event ID", "Fighter 1 ID", "Fighter 2 ID", "Outcome", "Rounds", "Method of Victory"]
            display_table(headers, fights)
        else:
            print(f"No fights found for Event ID {event_id}.")

# Query fighters in an event
def query_fighters_in_event():
    query_all_events()
    event_id = input("Enter the Event ID to view fighters: ")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT f.fighter_id, f.name, fe.result, fe.round
                          FROM Fighter f
                          JOIN Fighters_events fe ON f.fighter_id = fe.fighter_id
                          WHERE fe.event_id = ?;""", (event_id,))
        fighters = cursor.fetchall()
        if fighters:
            headers = ["Fighter ID", "Name", "Result", "Round"]
            display_table(headers, fighters)
        else:
            print(f"No fighters found for Event ID {event_id}.")

# Query statistics for a fighter
def query_statistics_for_fighter():
    query_all_fighters()
    fighter_id = input("Enter the Fighter ID to view statistics: ")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT s.name, fs.statistic_value
                          FROM Statistics s
                          JOIN Fighter_statistics fs ON s.statistic_id = fs.statistic_id
                          WHERE fs.fighter_id = ?;""", (fighter_id,))
        statistics = cursor.fetchall()
        if statistics:
            headers = ["Statistic", "Value"]
            display_table(headers, statistics)
        else:
            print(f"No statistics found for Fighter ID {fighter_id}.")

# Query all statistics
def query_all_statistics():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Statistics;")
        statistics = cursor.fetchall()
        if statistics:
            headers = ["Statistic ID", "Name"]
            display_table(headers, statistics)
        else:
            print("No statistics found.")

# Main menu
def main():
    initialize_database()
    while True:
        print("\n--- Knockout DB ---")
        print("1. Add Records (Fighter, Event, Fight, etc.)")
        print("2. View Records (Fighters, Events, Statistics, etc.)")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_records_menu()
        elif choice == "2":
            view_records_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Submenu for adding records
def add_records_menu():
    while True:
        print("\n--- Add Records ---")
        print("1. Add Fighter")
        print("2. Add Event")
        print("3. Add Fight")
        print("4. Add Participation (Fighters_Events)")
        print("5. Add Statistic")
        print("6. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_fighter()
        elif choice == "2":
            add_event()
        elif choice == "3":
            add_fight()
        elif choice == "4":
            add_participation()
        elif choice == "5":
            add_statistic()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")

# Submenu for viewing records
def view_records_menu():
    while True:
        print("\n--- View Records ---")
        print("1. View All Fighters")
        print("2. View All Events")
        print("3. View Fights in an Event")
        print("4. View Fighters in an Event")
        print("5. View Statistics for a Fighter")
        print("6. View All Statistics")
        print("7. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            query_all_fighters()
        elif choice == "2":
            query_all_events()
        elif choice == "3":
            query_fights_in_event()
        elif choice == "4":
            query_fighters_in_event()
        elif choice == "5":
            query_statistics_for_fighter()
        elif choice == "6":
            query_all_statistics()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
