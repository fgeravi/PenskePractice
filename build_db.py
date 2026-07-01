import json
import sqlite3

# Open JSON file
with open("race_data.json", "r") as file:
    data = json.load(file)

# Connecting to SQLite
conn = sqlite3.connect("race.db")
cursor = conn.cursor()

# Creating table
cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    name TEXT,
    car_number INTEGER,
    lap_time REAL,
    position INTEGER
)
""")

# Clear old data
cursor.execute("DELETE FROM drivers")

# Insert each driver
for driver in data["drivers"]:
    cursor.execute("""
    INSERT INTO drivers (name, car_number, lap_time, position)
    VALUES (?, ?, ?, ?)
    """, (
        driver["name"],
        driver["car_number"],
        driver["lap_time"],
        driver["position"]
    ))

conn.commit()
conn.close()

print("Database created")