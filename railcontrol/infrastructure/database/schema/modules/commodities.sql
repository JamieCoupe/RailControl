-- ==========================================================
-- Table: commodity
-- Purpose: Table for storing commodity data
-- Notes:
--   - part of module: industry
-- ==========================================================

CREATE TABLE commodity (
    id      VARCHAR(20) PRIMARY KEY,
    name    VARCHAR(255) NOT NULL,
    unit    VARCHAR(20)  NOT NULL,
    default_wagon_classification_id VARCHAR(20)   -- FK added in constraints
);
