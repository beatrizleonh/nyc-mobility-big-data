-- ============================================================
-- NYC Mobility Big Data
-- Carga de tablas analíticas en MariaDB
-- ============================================================

USE nyc_mobility;


-- 1. Resumen mensual
TRUNCATE TABLE monthly_summary;

LOAD DATA INFILE '/tmp/nyc_data/monthly_summary.csv'
INTO TABLE monthly_summary
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(year, month, total_trips, avg_trip_miles, avg_trip_minutes, avg_speed_mph);


-- 2. Resumen por hora
TRUNCATE TABLE hourly_summary;

LOAD DATA INFILE '/tmp/nyc_data/hourly_summary.csv'
INTO TABLE hourly_summary
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(pickup_hour, total_trips, avg_trip_minutes, avg_speed_mph);


-- 3. Resumen por día de la semana
TRUNCATE TABLE daily_summary;

LOAD DATA INFILE '/tmp/nyc_data/daily_summary.csv'
INTO TABLE daily_summary
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(day_of_week, total_trips, avg_trip_minutes, avg_speed_mph, day_name);


-- 4. Zonas principales de origen
TRUNCATE TABLE top_pickup_zones;

LOAD DATA INFILE '/tmp/nyc_data/top_pickup_zones.csv'
INTO TABLE top_pickup_zones
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(PULocationID, total_trips, avg_trip_minutes, avg_trip_miles);


-- 5. Zonas principales de destino
TRUNCATE TABLE top_dropoff_zones;

LOAD DATA INFILE '/tmp/nyc_data/top_dropoff_zones.csv'
INTO TABLE top_dropoff_zones
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(DOLocationID, total_trips, avg_trip_minutes, avg_trip_miles);


-- 6. Indicadores económicos mensuales
TRUNCATE TABLE monthly_economics;

LOAD DATA INFILE '/tmp/nyc_data/monthly_economics.csv'
INTO TABLE monthly_economics
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(year, month, avg_base_fare, avg_driver_pay, total_base_fare, total_driver_pay);


-- 7. Resumen anual
TRUNCATE TABLE annual_sql_summary;

LOAD DATA INFILE '/tmp/nyc_data/annual_sql_summary.csv'
INTO TABLE annual_sql_summary
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(year, annual_trips, avg_trip_miles, avg_trip_minutes, avg_speed_mph);