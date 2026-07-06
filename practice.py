drivers = [
    {
        "name": "Blaney",
        "car_number": 12,
        "laps": [30.1, 29.9, 30.0]
    },
    {
        "name": "Logano",
        "car_number": 22,
        "laps": [30.4, 30.2, 30.3]
    },
    {
        "name": "Cindric",
        "car_number": 2,
        "laps": [30.0, 29.8, 29.9]
    }
]

fastest_driver = ""
fastest_average = 999999

for driver in drivers:

    name = driver["name"]
    car_number = driver["car_number"]
    laps = driver["laps"]

    total_lap_time = 0

    for lap_time in laps:
        total_lap_time += lap_time

    average_lap_time = total_lap_time / len(laps)

    print(name, "Car", car_number, "Average:", average_lap_time)

    if average_lap_time < fastest_average:
        fastest_average = average_lap_time
        fastest_driver = name

print()
print("Fastest Driver:", fastest_driver)
print("Fastest Average:", fastest_average)