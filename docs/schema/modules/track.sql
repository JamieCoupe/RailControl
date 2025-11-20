-- ==========================================================
-- Table: track_section
-- Purpose: Physical track segments between junctions
-- Notes:
--   - start_junction_id, end_junction_id FKs added in constraints
-- ==========================================================

CREATE TABLE track_section (
    id                VARCHAR(20) PRIMARY KEY,
    name              VARCHAR(255),
    length_mm         INT         NOT NULL,
    start_junction_id VARCHAR(20),       -- FK in constraints (nullable)
    end_junction_id   VARCHAR(20),       -- FK in constraints (nullable)
    track_type        VARCHAR(20) NOT NULL,  -- -> track_section_type_enum
    max_speed_kph     INT
);

-- ==========================================================
-- Table: turnout
-- Purpose: Turnouts / switches at junctions
-- ==========================================================

CREATE TABLE turnout (
    id          VARCHAR(20) PRIMARY KEY,
    junction_id VARCHAR(20) NOT NULL,   -- FK in constraints
    name        VARCHAR(255)
);

-- ==========================================================
-- Table: turnout_leg
-- Purpose: Legs of a turnout (straight, diverging)
-- ==========================================================

CREATE TABLE turnout_leg (
    turnout_id      VARCHAR(20) NOT NULL,  -- FK in constraints
    track_section_id VARCHAR(20) NOT NULL, -- FK in constraints
    leg_type        VARCHAR(20) NOT NULL,  -- -> turnout_leg_enum

    PRIMARY KEY (turnout_id, track_section_id)
);

-- ==========================================================
-- Table: junction
-- Purpose: Nodes in the track graph
-- ==========================================================

CREATE TABLE junction (
    id            VARCHAR(20) PRIMARY KEY,
    name          VARCHAR(255),
    junction_type VARCHAR(20) NOT NULL,   -- -> junction_type_enum
    length_mm     INT
);

-- ==========================================================
-- Table: track_route
-- Purpose: Logical route (mainline, platform, industry spur etc)
-- ==========================================================

CREATE TABLE track_route (
    id         VARCHAR(20) PRIMARY KEY,
    name       VARCHAR(255),
    route_type VARCHAR(20) NOT NULL      -- -> track_route_type_enum
);

-- ==========================================================
-- Table: track_route_track_section
-- Purpose: Ordered list of sections making up a route
-- ==========================================================

CREATE TABLE track_route_track_section (
    id               VARCHAR(20) PRIMARY KEY,
    track_route_id   VARCHAR(20) NOT NULL,  -- FK in constraints
    track_section_id VARCHAR(20) NOT NULL,  -- FK in constraints
    sequence         INT         NOT NULL,
    direction        VARCHAR(20) NOT NULL,  -- -> direction_enum

    UNIQUE (track_route_id, track_section_id, direction)
);
