-- ==========================================================
-- Table: track_route
-- Purpose: Logical routing entity (station route, platform route, industry spur, etc.)
-- Notes:
--   - module: route
--   - type is an ENUM (mainline, platform, industry, siding, loop, etc.)
--   - subclass tables: platform_track_route, industry_track_route
-- ==========================================================

CREATE TABLE track_route (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255),
    route_type VARCHAR(20) NOT NULL      -- ENUM applied in Lesson 5
);

-- Relationship Notes:
--   track_route 1 -- 1 platform_track_route      (if type=platform)
--   track_route 1 -- 1 industry_track_route      (if type=industry)
--   track_route 1 -- 1..* track_route_track_section
--   track_route 1 -- 0..* station_track_route

-- ==========================================================
-- Table: platform_track_route
-- Purpose: Extra data for track routes representing station platforms
-- Notes:
--   - module: routing
--   - id is both PK and FK → track_route.id
-- ==========================================================

CREATE TABLE platform_track_route (
    id VARCHAR(20) PRIMARY KEY,          -- FK to track_route.id
    platform_number INT NOT NULL,
    dwell_time_minutes INT NOT NULL
);

-- Relationship Notes:
--   platform_track_route 1 -- 1 track_route  (inheritance)
--   station 1 -- 0..* platform_track_route

-- ==========================================================
-- Table: industry_track_route
-- Purpose: Extra data for track routes representing industry spurs or loading tracks
-- Notes:
--   - module: routing
--   - id is both PK and FK → track_route.id
-- ==========================================================

CREATE TABLE industry_track_route (
    id VARCHAR(20) PRIMARY KEY,        -- FK to track_route.id
    industry_id VARCHAR(20) NOT NULL,  -- FK added in Lesson 5
    load_time_minutes INT
);

-- Relationship Notes:
--   industry_track_route 1 -- 1 track_route   (inheritance)
--   industry 1 -- 0..* industry_track_route

-- ==========================================================
-- Table: station_track_route
-- Purpose: Connects stations to the track routes that pass through them
-- Notes:
--   - module: routing
--   - many-to-many relationship resolved through this table
-- ==========================================================

CREATE TABLE station_track_route (
    id VARCHAR(20) PRIMARY KEY,
    station_id VARCHAR(20) NOT NULL,
    track_route_id VARCHAR(20) NOT NULL
);

-- Relationship Notes:
--   station 1 -- 0..* station_track_route
--   track_route 1 -- 0..* station_track_route

-- ==========================================================
-- Table: track_route_track_section
-- Purpose: Defines which track sections belong to a route and in which order
-- Notes:
--   - module: routing
--   - sequence defines ordering
--   - direction is an ENUM (forward, reverse)
-- ==========================================================

CREATE TABLE track_route_track_section (
    id VARCHAR(20) PRIMARY KEY,
    track_route_id VARCHAR(20) NOT NULL,
    track_section_id VARCHAR(20) NOT NULL,
    sequence INT NOT NULL,
    direction VARCHAR(20) NOT NULL      -- ENUM {forward, reverse}
);

-- Relationship Notes:
--   track_route 1 -- 1..* track_route_track_section
--   track_section 1 -- 0..* track_route_track_section

