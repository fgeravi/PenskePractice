lap_times = [30.2, 29.9, 30.1, 29.8]

best = lap_times[0]

for lap in lap_times:
    if lap < best:
        best = lap

print(best)