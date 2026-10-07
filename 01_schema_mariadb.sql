-- ============================================================
-- NYC Mobility Big Data
-- Esquema de la capa analítica en MariaDB
-- ============================================================

CREATE DATABASE IF NOT EXISTS nyc_mobility;
USE nyc_mobility;


-- 1. Resumen mensual
CREATE TABLE IF NOT EXISTS monthly_summary (
    year INT NOT NULL,
    month INT NOT NULL,
    total_trips BIGINT NOT NULL,
    avg_trip_miles DECIMAL(10,2),
    avg_trip_minutes DECIMAL(10,2),
    avg_speed_mph DECIMAL(10,2),
    PRIMARY KEY (year, month)
);


-- 2. Resumen por hora
CREATE TABLE IF NOT EXISTS hourly_summary (
    pickup_hour INT NOT NULL,
    total_trips BIGINT NOT NULL,
    avg_trip_minutes DECIMAL(10,2),
    avg_speed_mph DECIMAL(10,2),
    PRIMARY KEY (pickup_hour)
);


-- 3. Resumen por día de la semana
CREATE TABLE IF NOT EXISTS daily_summary (
    day_of_week INT NOT NULL,
    total_trips BIGINT NOT NULL,
    avg_trip_minutes DECIMAL(10,2),
    avg_speed_mph DECIMAL(10,2),
    day_name VARCHAR(20),
    PRIMARY KEY (day_of_week)
);

-- 4. Zonas principales de origen
CREATE TABLE IF NOT EXISTS top_pickup_zones (
    PULocationID INT NOT NULL,
    total_trips BIGINT NOT NULL,
    avg_trip_minutes DECIMAL(10,2),
    avg_trip_miles DECIMAL(10,2),
    PRIMARY KEY (PULocationID)
);


-- 5. Zonas principales de destino
CREATE TABLE IF NOT EXISTS top_dropoff_zones (
    DOLocationID INT NOT NULL,
    total_trips BIGINT NOT NULL,
    avg_trip_minutes DECIMAL(10,2),
    avg_trip_miles DECIMAL(10,2),
    PRIMARY KEY (DOLocationID)
);


-- 6. Indicadores económicos mensuales
CREATE TABLE IF NOT EXISTS monthly_economics (
    year INT NOT NULL,
    month INT NOT NULL,
    avg_base_fare DECIMAL(12,2),
    avg_driver_pay DECIMAL(12,2),
    total_base_fare DECIMAL(20,2),
    total_driver_pay DECIMAL(20,2),
    PRIMARY KEY (year, month)
);


-- 7. Resumen anual generado mediante SQL
CREATE TABLE IF NOT EXISTS annual_sql_summary (
    year INT NOT NULL,
    annual_trips BIGINT NOT NULL,
    avg_trip_miles DECIMAL(10,2),
    avg_trip_minutes DECIMAL(10,2),
    avg_speed_mph DECIMAL(10,2),
    PRIMARY KEY (year)
);