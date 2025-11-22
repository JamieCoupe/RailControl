-- ==========================================================
-- Table: station
-- Purpose: Table for stations
-- Notes:
--   - part of module: stations
-- ==========================================================

CREATE TABLE station (
    id   VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- ==========================================================
-- Table: platform_track_block
-- Purpose: Extra data for track routes representing station platforms
-- Notes:
--   - part of module: stations
--   - id is both PK and FK → track_block.id (in constraints)
-- ==========================================================

CREATE TABLE platform_track_block (
    id                 VARCHAR(20) PRIMARY KEY,  -- FK in constraints
    platform_number    INT         NOT NULL,
    dwell_time_minutes INT         NOT NULL
);

-- ==========================================================
-- Table: station_track_block
-- Purpose: Connects stations to the track routes that pass through them
-- Notes:
--   - part of module: stations
-- ==========================================================

CREATE TABLE station_track_block (
    station_id    VARCHAR(20) NOT NULL,   -- FK in constraints
    track_block_id VARCHAR(20) NOT NULL,  -- FK in constraints

    PRIMARY KEY (station_id, track_block_id)
);
