def tire_needs_change(tread_depth):
    if tread_depth <= 3:
        return "Change"
    if tread_depth > 3 and tread_depth <= 5:
        return "Inspect soon"
    if tread_depth > 5:
        return "Good"
    
print(tire_needs_change(3.5))
    