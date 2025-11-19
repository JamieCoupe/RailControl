-- ==========================================================
-- Table: industry
-- Purpose: Table for industries
-- Notes:
--   - part of module:industry
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

-- ==========================================================
-- Table: industry_input
-- Purpose: Table for industry input
-- Notes:
--   - part of module:industry
--   - related tables: industry, commodity
-- ==========================================================

CREATE TABLE industry_input (
    commodity_id VARCHAR(20)
        REFERENCES commodity(id) ON DELETE RESTRICT,
    industry_id VARCHAR(20)
        REFERENCES industry(id) ON DELETE CASCADE,
    amount int NOT NULL,

    PRIMARY KEY (commodity_id, industry_id)
);

-- Relationship Notes:
--   industry 1 -- 0..* industry_input
--   commodity 1 -- 0..* industry_input

-- ==========================================================
-- Table: industry_output
-- Purpose: Table for industry output
-- Notes:
--   - part of module:industry
--   - related tables: industry, commodity
-- ==========================================================

CREATE TABLE industry_output (
    commodity_id VARCHAR(20)
        REFERENCES commodity(id) ON DELETE RESTRICT,
    industry_id VARCHAR(20)
        REFERENCES industry(id) ON DELETE CASCADE,
    amount int NOT NULL,

    PRIMARY KEY (commodity_id, industry_id)
);
-- Relationship Notes:
--   industry 1 -- 0..* industry_output
--   commodity 1 -- 0..* industry_output

-- ==========================================================
-- Table: industry_track_route
-- Purpose: Extra data for track routes representing industry spurs or loading tracks
-- Notes:
--   - module: industry
--   - id is both PK and FK → track_route.id
-- ==========================================================

CREATE TABLE industry_track_route (
    id VARCHAR(20) PRIMARY KEY         -- also FK → track_route.id
        REFERENCES track_route(id) ON DELETE CASCADE,
    load_time_minutes INT
);

-- ==========================================================
-- Table: industry_track_route_map
-- Purpose: Extra data for track routes representing industry spurs or loading tracks
-- Notes:
--   - module: industry
--   - id is both PK and FK → track_route.id
-- ==========================================================

CREATE TABLE industry_track_route_map  (
    industry_id VARCHAR(20) NOT NULL
        REFERENCES industry(id) ON DELETE CASCADE,
    track_route_id VARCHAR(20) NOT NULL
        REFERENCES track_route(id) ON DELETE CASCADE,

    PRIMARY KEY (industry_id, track_route_id)
);

-- Relationship Notes:
--   industry_track_route_map  1 -- 1 track_route   (inheritance)
--   industry 1 -- 0..* industry_track_route

