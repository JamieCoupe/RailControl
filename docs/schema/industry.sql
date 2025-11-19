-- ==========================================================
-- Table: Commodity
-- Purpose: Table for storing commodity data
-- Notes:
--   - part of module:industry
--   - relates to WagonClassification, IndustryInput, IndustryOutput, wagonCompatabilityCommodity
-- ==========================================================

CREATE TABLE commodity (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    default_wagon_classification_id VARCHAR(20)
);

-- Relationship Notes:
--   commodity 1 -- 0..* wagon_compatible_commodity
--   commodity 1 -- 0..* industry_input
--   commodity 1 -- 0..* industry_output
--   commodity.default_wagon_classification_id -> wagon_classification.id

-- ==========================================================
-- Table: industry_input
-- Purpose: Table for industry input
-- Notes:
--   - part of module:stock
--   - related tables: industry, commodity
-- ==========================================================

CREATE TABLE industry_input (
    commodity_id VARCHAR(20),
    industry_id VARCHAR(20),
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
--   - part of module:locations
--   - related tables: industry, commodity
-- ==========================================================

CREATE TABLE industry_output (
    commodity_id VARCHAR(20),
    industry_id VARCHAR(20),
    amount int NOT NULL,

    PRIMARY KEY (commodity_id, industry_id)
);
-- Relationship Notes:
--   industry 1 -- 0..* industry_output
--   commodity 1 -- 0..* industry_output