# Fuel strategy practice program

# Intended to change for each track
TOTAL_LAPS = 250
FUEL_WINDOW = 55
GALLONS_PER_TANK = 18.0

# OPTIONS:
# "finish_attack" = minimum fuel, aggressive, light car
# "track_position" = still short fuel, but safer buffer
# "balanced" = gain positions
PRIORITY = "finish_attack"


def make_fuel_strategy(total_laps, fuel_window):
    pit_laps = []
    current_lap = fuel_window

    while current_lap < total_laps:
        pit_laps.append(current_lap)
        current_lap += fuel_window

    return pit_laps


def gallons_needed(laps_needed, fuel_window, gallons_per_tank):
    gallons_per_lap = gallons_per_tank / fuel_window
    return laps_needed * gallons_per_lap


def get_fuel_buffer(priority):
    if priority == "finish_attack":
        return 0.5
    elif priority == "track_position":
        return 3.0
    elif priority == "balanced":
        return 1.5
    else:
        return 1.5


def print_strategy(total_laps, fuel_window, gallons_per_tank, priority):
    pit_laps = make_fuel_strategy(total_laps, fuel_window)

    print("****** FUEL STRATEGY ******")
    print(f"Race length: {total_laps} laps")
    print(f"Fuel window: {fuel_window} laps")
    print(f"Full tank: {gallons_per_tank} gallons")
    print(f"Priority: {priority}")
    print(f"Total pit stops needed: {len(pit_laps)}")
    print()

    if len(pit_laps) == 0:
        print("No pit stops needed.")
        return

    previous_lap = 0

    for pit_number, pit_lap in enumerate(pit_laps, start=1):
        run_length = pit_lap - previous_lap
        fuel_used = gallons_needed(run_length, fuel_window, gallons_per_tank)

        print(f"Run {pit_number}: Lap {previous_lap} to Lap {pit_lap}")
        print(f"  Fuel used: {fuel_used:.2f} gallons")
        print(f"  Pit stop {pit_number}: Lap {pit_lap}")
        print()

        previous_lap = pit_lap

    final_run = total_laps - pit_laps[-1]
    final_fuel_needed = gallons_needed(final_run, fuel_window, gallons_per_tank)
    fuel_buffer = get_fuel_buffer(priority)
    recommended_fuel = final_fuel_needed + fuel_buffer

    if recommended_fuel > gallons_per_tank:
        recommended_fuel = gallons_per_tank

    print("Final run:")
    print(f"  Laps after last pit: {final_run}")
    print(f"  Fuel needed to finish: {final_fuel_needed:.2f} gallons")
    print(f"  Fuel buffer: {fuel_buffer:.2f} gallons")
    print(f"  RECOMMENDED FINAL FUEL: {recommended_fuel:.2f} gallons")

    if priority == "finish_attack":
        print("  Strategy note: Aggressive and low on fuel for weight redution")
    elif priority == "track_position":
        print("  Strategy note: Safer. Still lighter than full fuel, but with extra margin.")
    else:
        print("  Strategy note: Balanced fuel risk, looking for position gain.")


print_strategy(TOTAL_LAPS, FUEL_WINDOW, GALLONS_PER_TANK, PRIORITY)