-- ==========================================================
-- Table: track_section
-- Purpose: Stores the physical track segments between junctions
-- Notes:
--   - module: track
--   - related tables: junction, track_route_track_section
--   - each section may have:
--       • 0–1 start junction
--       • 0–1 end junction
-- ==========================================================

CREATE TABLE track_section (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255),
    length_mm INT NOT NULL,
    start_junction_id VARCHAR(20)
        REFERENCES junction(id) ON DELETE RESTRICT,   -- nullable
    end_junction_id VARCHAR(20)     -- nullable
        REFERENCES junction(id) ON DELETE RESTRICT,
    track_type VARCHAR(20) NOT NULL, -- ENUM applied later
    max_speed_kph INT                -- optional speed limit
);

-- Relationship Notes:
--   junction 1 -- 0..* track_section (as start_junction)
--   junction 1 -- 0..* track_section (as end_junction)
--   track_section 0..1 -- 1 junction (start)
--   track_section 0..1 -- 1 junction (end)
--   track_section 1 -- 0..* track_route_track_section

-- ==========================================================
-- Table: turnout
-- Purpose: Represents a turnout/switch located at a junction
-- Notes:
--   - module: track
--   - related tables: turnout_leg, junction
-- ==========================================================

CREATE TABLE turnout (
    id VARCHAR(20) PRIMARY KEY,
    junction_id VARCHAR(20) NOT NULL
        REFERENCES junction(id) ON DELETE RESTRICT,
    name VARCHAR(255)
);

-- Relationship Notes:
--   junction 1 -- 0..* turnout
--   turnout 1 -- 2..* turnout_leg   (composition)

-- ==========================================================
-- Table: turnout_leg
-- Purpose: Legs of a turnout (straight, diverging)
-- Notes:
--   - module: track
--   - relates to: turnout, track_section
-- ==========================================================

CREATE TABLE turnout_leg (
    turnout_id VARCHAR(20) NOT NULL
        REFERENCES turnout(id) ON DELETE CASCADE,
    track_section_id VARCHAR(20) NOT NULL
        REFERENCES track_section(id) ON DELETE RESTRICT ,
    leg_type VARCHAR(20) NOT NULL,   -- ENUM: straight, diverging, optional others

    PRIMARY KEY (turnout_id, track_section_id)
);

-- Relationship Notes:
--   turnout 1 -- 2..* turnout_leg        (composition)
--   track_section 1 -- 0..* turnout_leg

-- ==========================================================
-- Table: junction
-- Purpose: Stores all track junctions (nodes in the track graph)
-- Notes:
--   - module: track
--   - junction_type is an ENUM applied later
--   - related tables: track_section, turnout
-- ==========================================================

CREATE TABLE junction (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255),
    junction_type VARCHAR(20) NOT NULL,    -- ENUM added in Lesson 6
    length_mm INT
);

-- Relationship Notes:
--   junction 1 -- 0..* track_section (start)
--   junction 1 -- 0..* track_section (end)
--   junction 1 -- 0..* turnout

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


-- Relationship Notes:
--   industry_track_route 1 -- 1 track_route   (inheritance)
--   industry 1 -- 0..* industry_track_route

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
    track_route_id VARCHAR(20) NOT NULL
        REFERENCES track_route(id) ON DELETE CASCADE,
    track_section_id VARCHAR(20) NOT NULL
        REFERENCES track_section(id) ON DELETE RESTRICT,
    sequence INT NOT NULL,
    direction VARCHAR(20) NOT NULL,      -- ENUM {forward, reverse}

    UNIQUE (track_route_id, track_section_id, direction)
);

-- Relationship Notes:
--   track_route 1 -- 1..* track_route_track_section
--   track_section 1 -- 0..* track_route_track_section
--   track_route 1 -- 1..* track_route_track_section
--   track_section 1 -- 0..* track_route_track_section
