import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

slowest_lap = 0

for driver in drivers:
    if driver["lap_time"] > slowest_lap:
        slowest_lap = driver["lap_time"]

print("Slowest Driver: ", driver["name"])