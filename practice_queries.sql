SELECT * FROM drivers;

SELECT name, lap_time
FROM drivers
ORDER BY lap_time ASC;

SELECT name
FROM drivers
WHERE lap_time < 30;