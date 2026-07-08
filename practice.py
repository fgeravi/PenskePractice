def estimate_pit_stops(total_laps, fuel_per_tank):
    stops = total_laps // fuel_per_tank

    if total_laps % fuel_per_tank != 0:
        stops += 1

    print(f"Race Distance: {total_laps}")
    print(f"Fuel Window: {fuel_per_tank}")
    print(f"Estimated Stops: {stops - 1}")


    estimate_pit_stops(400, 65)