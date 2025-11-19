-- ==========================================================
-- Table: station
-- Purpose: Table for stations
-- Notes:
--   - part of module:stations
--   - related tables: platform_track_route, track_route
-- ==========================================================

CREATE TABLE station (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Relationship Notes:
--   station 1 -- 0..* station_track_route


-- ==========================================================
-- Table: platform_track_route
-- Purpose: Extra data for track routes representing station platforms
-- Notes:
--   - module: stations
--   - id is both PK and FK → track_route.id
-- ==========================================================

CREATE TABLE platform_track_route (
    id VARCHAR(20) PRIMARY KEY
        REFERENCES track_route(id) ON DELETE CASCADE,
    platform_number INT NOT NULL,
    dwell_time_minutes INT NOT NULL
);

-- Relationship Notes:
--   platform_track_route 1 -- 1 track_route  (inheritance)
--   station 1 -- 0..* platform_track_route


-- ==========================================================
-- Table: station_track_route
-- Purpose: Connects stations to the track routes that pass through them
-- Notes:
--   - module: stations
--   - many-to-many relationship resolved through this table
-- ==========================================================

CREATE TABLE station_track_route (
    station_id VARCHAR(20) NOT NULL
        References station(id) ON DELETE CASCADE,
    track_route_id VARCHAR(20) NOT NULL
         REFERENCES track_route(id) ON DELETE CASCADE,

    PRIMARY KEY (station_id, track_route_id)
);

-- Relationship Notes:
--   station 1 -- 0..* station_track_route
--   track_route 1 -- 0..* station_track_route
