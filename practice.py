import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

total_time = 0

for driver in drivers:
    total_time = total_time + driver["lap_time"]
    average_time = total_time / len(drivers)

print("Average lap time: ", average_time)
