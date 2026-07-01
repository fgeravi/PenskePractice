import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

sorted_drivers = sorted(drivers, key=lambda driver: driver["car_number"])

for driver in sorted_drivers:
    print(driver["car_number"], "-", driver["name"])