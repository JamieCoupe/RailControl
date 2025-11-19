-- ==========================================================
-- Table: wagon_classification
-- Purpose: Table for wagon classification
-- Notes:
--   - part of module:stock
--   - wagon_type is an ENUM (not a related table)
--   - related tables: wagon, wagon_compatible_commodity
-- ==========================================================

CREATE TABLE wagon_classification (
    id VARCHAR(20) PRIMARY KEY,
    classification_code VARCHAR(10) NOT NULL,
    wagon_type VARCHAR(20) NOT NULL,
    length_mm int NOT NULL
);

-- Relationship Notes:
--   wagon_classification 1 -- 0..* wagon
--   wagon_classification 1 -- 0..* wagon_compatible_commodity

-- ==========================================================
-- Table: wagon_compatible_commodity
-- Purpose: Table for compatibility of wagons with commodities
-- Notes:
--   - part of module:stock
--   - related tables: wagon_classification, commodity
-- ==========================================================

CREATE TABLE wagon_compatible_commodity (
    id VARCHAR(20) PRIMARY KEY,
    commodity_id VARCHAR(20) NOT NULL
        REFERENCES commodity(id) ON DELETE RESTRICT,
    wagon_classification_id VARCHAR(20) NOT NULL
        REFERENCES wagon_classification(id) ON DELETE RESTRICT,
);

-- Relationship Notes:
--   commodity  1 -- 0..* wagon_compatible_commodity
--   wagon_classification 1 -- 0..* wagon_compatible_commodity

-- ==========================================================
-- Table: wagon
-- Purpose: Table for wagons
-- Notes:
--   - part of module:stock
--   - related tables: wagon, wagon_classification
-- ==========================================================

CREATE TABLE wagon (
    id VARCHAR(20) PRIMARY KEY,
    running_number VARCHAR(36) NOT NULL,
    wagon_classification_id VARCHAR(20) NOT NULL
        REFERENCES wagon_classification(id) ON DELETE RESTRICT,
    capacity int NOT NULL
);

-- Relationship Notes:
--   wagon_classification 1 -- 0..* wagons
