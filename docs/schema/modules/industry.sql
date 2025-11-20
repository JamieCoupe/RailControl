-- ==========================================================
-- Table: industry
-- Purpose: Table for industries
-- Notes:
--   - part of module: industry
--   - type becomes industry_type_enum in enums.sql
-- ==========================================================

CREATE TABLE industry (
    id   VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20)  NOT NULL
);

-- ==========================================================
-- Table: industry_input
-- Purpose: Commodities consumed by industries
-- ==========================================================

CREATE TABLE industry_input (
    commodity_id VARCHAR(20) NOT NULL,  -- FK in constraints
    industry_id  VARCHAR(20) NOT NULL,  -- FK in constraints
    amount       INT         NOT NULL,

    PRIMARY KEY (commodity_id, industry_id)
);

-- ==========================================================
-- Table: industry_output
-- Purpose: Commodities produced by industries
-- ==========================================================

CREATE TABLE industry_output (
    commodity_id VARCHAR(20) NOT NULL,  -- FK in constraints
    industry_id  VARCHAR(20) NOT NULL,  -- FK in constraints
    amount       INT         NOT NULL,

    PRIMARY KEY (commodity_id, industry_id)
);

-- ==========================================================
-- Table: industry_track_route
-- Purpose: Child table for track routes that are industry spurs
-- Notes:
--   - id is PK; becomes FK → track_route.id in constraints
-- ==========================================================

CREATE TABLE industry_track_route (
    id                VARCHAR(20) PRIMARY KEY,
    load_time_minutes INT
);

-- ==========================================================
-- Table: industry_track_route_map
-- Purpose: Links industries to their industry routes
-- ==========================================================

CREATE TABLE industry_track_route_map (
    industry_id   VARCHAR(20) NOT NULL,  -- FK in constraints
    track_route_id VARCHAR(20) NOT NULL, -- FK in constraints

    PRIMARY KEY (industry_id, track_route_id)
);
