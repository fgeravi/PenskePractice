import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

count = 0

for driver in drivers:
    if driver["lap_time"] < 30:
        count = count + 1

print("Driver count under 30 seconds: ", count)
