# Train-Seat-Reservation-System-Optimization
Objective: 

To develop a train seat reservation system that optimizes seat allocation by reassigning available seats dynamically based on passenger routes, ensuring efficient utilization of seats and minimizing wasted space.

Problem Statement:

In a train seat reservation system, passengers board and leave the train at various stations along the route. A common issue in such systems is the inefficient use of seats, where new passengers are assigned new seats even when seats vacated by other passengers could be reused. This leads to wasted space and inefficient seat allocation. I noticed this issue while traveling from Ankara to Istanbul, where I noticed that people would not have an efficient seating order. I could write a code to optimize it to create greater profit and improve user experience.

Problem: 

The goal is to ensure that seats are optimally utilized by dynamically reassigning seats that become available when passengers disembark at intermediate stations. Specifically, when a passenger leaves a seat at a station, that seat should be assigned to a new passenger boarding at that station if their route allows it.

Solution:

The solution involves developing a Python script with an SQLite database to manage seat assignments. The script performs the following tasks:

Database Management:

* Creates an SQLite database to store seat assignments with details such as seat row, seat column, start station, end station, and passenger ID.

*Provides functionality to clear the database if needed.

Seat Assignment Logic:

* Checks for seats that become available at the start station of a new passenger's journey.
* Ensures that a seat is only reassigned if it is free for the entire journey of the new passenger.
* If no suitable seats are available, assign a new seat from the pool of unoccupied seats.

User Interaction:

* Prompts the user to input the start and end stations for each passenger and the number of passengers.
* Provides an option to clear the database before starting a new session.
* Displays the current state of the seat assignments in the database.

Use Case Scenario Example:

Passenger 1 books a seat from station A to station B (seat 1A).
Passenger 2 books a seat from station B to station D. Instead of assigning a new seat, the system should recognize that seat 1A becomes available at station B and reassign Passenger 2 to seat 1A.
The system ensures that seats are reused efficiently, preventing wastage of space and optimizing seat allocation.

Benefits:

* Efficiency: Maximizes the use of available seats, ensuring that seats are not left unoccupied unnecessarily.
* Scalability: Can handle multiple passengers and various start and end stations dynamically.
* User-Friendly: Provides clear prompts and outputs for users, making the reservation process straightforward.
