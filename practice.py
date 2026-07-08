class Part:

    def __init__(self, part_id, name, max_life):
        self.part_id = part_id
        self.name = name
        self.max_life = max_life
        self.current_miles = 0
        self.race_driven = False

    def add_miles(self, miles):
        self.current_miles += miles

    def mark_race_driven(self):
        self.race_driven = True

    def remaining(self):
        return self.max_life - self.current_miles

    def percent_used(self):
        return (self.current_miles / self.max_life) * 100

    def status(self):
        percent = self.percent_used()

        if percent >= 100:
            return "REPLACE NOW"
        elif percent >= 85:
            return "NEAR LIMIT"
        elif percent >= 60:
            return "MONITOR"
        else:
            return "GOOD"

    def display_report(self):
        print("\n===== PART LIFE REPORT =====")
        print("Part:", self.name)
        print("Part ID:", self.part_id)
        print("Miles Used:", self.current_miles)
        print("Life Limit:", self.max_life)
        print("Miles Remaining:", self.remaining())
        print(f"Life Used: {self.percent_used():.1f}%")
        print("Status:", self.status())

        if self.race_driven:
            print("Race Driven: YES")
            print("Warning: This part was race driven. Inspect for possible impact damage, fatigue, or abnormal wear.")
        else:
            print("Race Driven: NO")

        print("============================")


# Hardcoded standard part lifetimes
PART_LIFETIMES = {
    "Control Arm": 1200,
    "Coil Spring": 800,
    "Differential": 2500,
    "Shock Absorber": 1000,
    "Wheel Bearing": 600,
    "Driveshaft": 2000,
    "Brake Rotor": 500
}


parts = []


while True:

    print("\n===== NASCAR PARTS LIFE TRACKER =====")
    print("1. Add New Part")
    print("2. Add Miles to Part")
    print("3. View All Parts")
    print("4. Quit")

    choice = input("Choose: ")

    if choice == "1":

        print("\nChoose Part Type:")

        part_names = list(PART_LIFETIMES.keys())

        for i in range(len(part_names)):
            print(f"{i + 1}. {part_names[i]} - {PART_LIFETIMES[part_names[i]]} mile life")

        selected = int(input("Enter part number: "))

        if selected < 1 or selected > len(part_names):
            print("Invalid selection.")
            continue

        name = part_names[selected - 1]
        life = PART_LIFETIMES[name]

        part_id = input("Enter Part ID / Serial Number: ")

        new_part = Part(part_id, name, life)
        parts.append(new_part)

        print(f"{name} added with a {life} mile life limit.")

    elif choice == "2":

        search = input("Enter Part ID: ")
        found = False

        for part in parts:
            if part.part_id == search:
                found = True

                miles = int(input("Miles to add: "))
                part.add_miles(miles)

                race_input = input("Was this part race driven? yes/no: ").lower()

                if race_input == "yes":
                    part.mark_race_driven()

                part.display_report()

        if not found:
            print("Part not found.")

    elif choice == "3":

        if len(parts) == 0:
            print("No parts entered yet.")
        else:
            for part in parts:
                part.display_report()

    elif choice == "4":
        break

    else:
        print("Invalid choice.")