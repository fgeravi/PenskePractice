import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

fastest_driver = drivers[0]

for driver in drivers:
    if driver["lap_time"] < fastest_driver["lap_time"]:
        fastest_driver = driver

print("Fastest driver: ", fastest_driver["name"])
print("Lap Time: ", fastest_driver["lap_time"])
        