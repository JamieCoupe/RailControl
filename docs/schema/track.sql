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
    start_junction_id VARCHAR(20),   -- nullable
    end_junction_id VARCHAR(20),     -- nullable
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
    start_junction_id VARCHAR(20),   -- nullable
    end_junction_id VARCHAR(20),     -- nullable
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
    junction_id VARCHAR(20) NOT NULL,       -- FK added in Lesson 5
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
    id VARCHAR(20) PRIMARY KEY,
    turnout_id VARCHAR(20) NOT NULL,
    track_section_id VARCHAR(20) NOT NULL,
    leg_type VARCHAR(20) NOT NULL   -- ENUM: straight, diverging, optional others
);

-- Relationship Notes:
--   turnout 1 -- 2..* turnout_leg        (composition)
--   track_section 1 -- 0..* turnout_leg
