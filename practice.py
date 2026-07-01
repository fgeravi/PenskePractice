import json

with open("race_data.json", "r") as file:
    data = json.load(file)

drivers = data["drivers"]

winner = ""

for driver in drivers:
    if driver["position"] == 1:
        winner = driver["name"]
        
print("Winning driver: ", winner)
