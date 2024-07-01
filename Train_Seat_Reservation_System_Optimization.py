import os
import sqlite3

# Define the number of rows and columns
rows = 15
columns = 4

# Define station names
stations = ["A", "B", "C", "D"]

# Define the path to the database
db_path = r"C:\Users\seymu\Desktop\Train\Train_seat_database.db"

# Ensure the directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create or connect to the SQLite database
try:
    conn = sqlite3.connect(db_path)
except sqlite3.OperationalError as e:
    print(f"Error opening database file: {e}")
    exit(1)

cursor = conn.cursor()


def recreate_table():
    cursor.execute('DROP TABLE IF EXISTS train_seats')
    cursor.execute('''CREATE TABLE train_seats (
                        Seat_Row INTEGER,
                        Seat_Column TEXT,
                        Start_Station TEXT,
                        End_Station TEXT,
                        Passenger_ID INTEGER,
                        PRIMARY KEY (Seat_Row, Seat_Column, Start_Station, End_Station)
                    )''')
    conn.commit()


def clear_seat_data():
    cursor.execute('DELETE FROM train_seats')
    conn.commit()


def assign_seat(start_station, end_station, passenger_id):
    start_index = stations.index(start_station)
    end_index = stations.index(end_station)

    # Check for seats becoming available at the start station
    cursor.execute('''SELECT Seat_Row, Seat_Column FROM train_seats 
                      WHERE End_Station = ?''', (start_station,))
    available_seats = cursor.fetchall()

    for seat in available_seats:
        row, column = seat
        # Check if the seat is occupied for the new route
        cursor.execute('''SELECT * FROM train_seats 
                          WHERE Seat_Row = ? AND Seat_Column = ? AND
                          ((Start_Station <= ? AND End_Station > ?) OR
                           (Start_Station < ? AND End_Station >= ?) OR
                           (? < Start_Station AND ? > End_Station))''',
                       (
                       row, column, start_station, start_station, end_station, end_station, start_station, end_station))

        if not cursor.fetchone():
            cursor.execute('''INSERT INTO train_seats (Seat_Row, Seat_Column, Start_Station, End_Station, Passenger_ID) 
                              VALUES (?, ?, ?, ?, ?)''', (row, column, start_station, end_station, passenger_id))
            conn.commit()
            return (row, column)

    # If no available seats, assign a new seat
    for row in range(1, rows + 1):
        for col in range(columns):
            column_letter = chr(ord('A') + col)
            seat = (row, column_letter)

            cursor.execute('''SELECT * FROM train_seats 
                              WHERE Seat_Row = ? AND Seat_Column = ? AND
                              ((Start_Station <= ? AND End_Station > ?) OR
                               (Start_Station < ? AND End_Station >= ?) OR
                               (? < Start_Station AND ? > End_Station))''',
                           (row, column_letter, start_station, start_station, end_station, end_station, start_station,
                            end_station))

            if not cursor.fetchone():
                cursor.execute('''INSERT INTO train_seats (Seat_Row, Seat_Column, Start_Station, End_Station, Passenger_ID) 
                                  VALUES (?, ?, ?, ?, ?)''',
                               (row, column_letter, start_station, end_station, passenger_id))
                conn.commit()
                return seat
    return None


def get_station_index(station):
    return stations.index(station)


def main():
    clear_table = input("Do you want to clear the SQL table? (y/n): ").lower()
    if clear_table == 'y':
        recreate_table()
        start_passenger_id = 1
    else:
        cursor.execute("SELECT MAX(Passenger_ID) FROM train_seats")
        max_id = cursor.fetchone()[0]
        start_passenger_id = (max_id or 0) + 1

    start_station = input("Enter the start station (A, B, C, D): ").upper()
    end_station = input("Enter the end station (A, B, C, D): ").upper()
    passenger_count = int(input("Enter the number of passengers: "))

    start_index = get_station_index(start_station)
    end_index = get_station_index(end_station)

    if start_index >= end_index:
        print("Invalid route. Start station must be before end station.")
        return

    for i in range(passenger_count):
        passenger_id = start_passenger_id + i
        seat = assign_seat(start_station, end_station, passenger_id)
        if seat:
            print(f"Passenger {passenger_id} seat: {seat[0]}{seat[1]}")
        else:
            print("No available seats for the specified route.")
            break

    show_table = input("Do you want to see the contents of the SQL table? (y/n): ").lower()
    if show_table == 'y':
        cursor.execute("SELECT * FROM train_seats")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
conn.close()
