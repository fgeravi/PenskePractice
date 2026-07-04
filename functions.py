def faster_driver(driver1, time1, driver2, time2):
    if time1 < time2:
        return driver1
    else:
        return driver2
    
print(faster_driver("Logano", 30, "Blaney", 40))