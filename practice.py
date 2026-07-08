tires = [
    {"set": "A12", "compound": "Soft", "laps": 22},
    {"set": "B07", "compound": "Medium", "laps": 5},
    {"set": "C03", "compound": "Hard", "laps": 48},
]

def find_freshest_tire(tires):
    freshest = min(tires, key=lambda tire: tire["laps"])

    print("Freshest Tire")
    print(f"Set: {freshest['set']}")
    print(f"Compound: {freshest['compound']}")
    print(f"Laps: {freshest['laps']}")