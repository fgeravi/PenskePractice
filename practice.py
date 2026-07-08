parts = [
    {"name": "Brake Rotor", "used": 420, "limit": 500},
    {"name": "Hub Bearing", "used": 175, "limit": 300},
    {"name": "Steering Rack", "used": 290, "limit": 300},
]

def parts_needing_service(parts):
    print("=== Parts Near Service ===")

    for part in parts:
        percent = (part["used"] / part["limit"]) * 100

        if percent >= 90:
            print(f"{part['name']} ({percent:.1f}% used)")