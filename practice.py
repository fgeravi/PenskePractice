import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

for driver in drivers:
    for key, value in driver.items():
        print(key, ":", value)