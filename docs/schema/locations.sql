-- ==========================================================
-- Table: station
-- Purpose: Table for stations
-- Notes:
--   - part of module:locations
--   - related tables: platform_track_route, track_route
-- ==========================================================

CREATE TABLE station (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Relationship Notes:
--   station 1 -- 0..* station_track_route

-- ==========================================================
-- Table: industry
-- Purpose: Table for industries
-- Notes:
--   - part of module:locations
--   - type is an ENUM
--   - related tables: industry_track_route (via industry_track_route), industry_input, industry_output
-- ==========================================================

CREATE TABLE industry (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL
);

-- Relationship Notes:
--   industry 1 -- 1..* industry_track_route
--   industry 1 -- 0..* industry_input
--   industry 1 -- 0..* industry_output
