-- ==========================================================
-- Table: wagon_classification
-- Purpose: Table for wagon classification
-- Notes:
--   - part of module: stock
-- ==========================================================

CREATE TABLE wagon_classification (
    id                  VARCHAR(20) PRIMARY KEY,
    classification_code VARCHAR(10) NOT NULL,
    wagon_type          VARCHAR(20) NOT NULL,   -- -> wagon_type_enum (enums.sql)
    length_mm           INT         NOT NULL
);

-- ==========================================================
-- Table: wagon_compatible_commodity
-- Purpose: Compatibility of wagon classifications with commodities
-- Notes:
--   - part of module: stock
-- ==========================================================

CREATE TABLE wagon_compatible_commodity (
    compat_id               VARCHAR(20) PRIMARY KEY,
    commodity_id            VARCHAR(20) NOT NULL,  -- FK in constraints
    wagon_classification_id VARCHAR(20) NOT NULL   -- FK in constraints
);

-- ==========================================================
-- Table: wagon
-- Purpose: Table for wagons
-- Notes:
--   - part of module: stock
-- ==========================================================

CREATE TABLE wagon (
    id                      VARCHAR(20) PRIMARY KEY,
    running_number          VARCHAR(36) NOT NULL,
    wagon_classification_id VARCHAR(20) NOT NULL,  -- FK in constraints
    capacity                INT         NOT NULL
);
