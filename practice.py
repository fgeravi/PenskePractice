drivers = [
    {"name": "Blaney", "position": 2},
    {"name": "Logano", "position": 5},
    {"name": "Byron", "position": 1},
    {"name": "Bell", "position": 3}
]

drivers.sort(key=lambda driver: driver["position"])

for driver in drivers:
    print(driver["name"], driver["position"])