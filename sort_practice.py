# Sorting practice

drivers = [
    {"name": "Blaney", "car_number": 12, "lap_time": 29.88, "position": 2},
    {"name": "Logano", "car_number": 22, "lap_time": 30.05, "position": 1},
    {"name": "Cindric", "car_number": 2, "lap_time": 30.12, "position": 4},
    {"name": "McLaughlin", "car_number": 3, "lap_time": 29.95, "position": 3}
]

print("Original driver list:")
for driver in drivers:
    print(driver)

print("\nSorted by fastest lap time:")
by_lap_time = sorted(drivers, key=lambda driver: driver["lap_time"])
for driver in by_lap_time:
    print(driver["name"], driver["lap_time"])

print("\nSorted by race position:")
by_position = sorted(drivers, key=lambda driver: driver["position"])
for driver in by_position:
    print(driver["position"], driver["name"])

print("\nSorted by car number:")
by_car_number = sorted(drivers, key=lambda driver: driver["car_number"])
for driver in by_car_number:
    print(driver["car_number"], driver["name"])

fastest_driver = min(drivers, key=lambda driver: driver["lap_time"])
print("\nFastest driver:")
print(fastest_driver["name"], fastest_driver["lap_time"])

slowest_driver = max(drivers, key=lambda driver: driver["lap_time"])
print("\nSlowest driver:")
print(slowest_driver["name"], slowest_driver["lap_time"])
