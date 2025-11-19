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
        REFERENCES wagon_classification(id) ON DELETE SET NULL
);

-- Relationship Notes:
--   commodity 1 -- 0..* wagon_compatible_commodity
--   commodity 1 -- 0..* industry_input
--   commodity 1 -- 0..* industry_output
--   commodity.default_wagon_classification_id -> wagon_classification.id
