-- Unique constraint on industry name
ALTER TABLE industry
ADD CONSTRAINT uq_industry_name UNIQUE (name);

-- FK from commodity → wagon_classification (default classification)
ALTER TABLE commodity
ADD CONSTRAINT fk_commodity_default_wagon_classification
FOREIGN KEY (default_wagon_classification_id)
REFERENCES wagon_classification(id)
ON DELETE SET NULL;

-- Industry input FKs + CHECK
ALTER TABLE industry_input
ADD CONSTRAINT fk_industry_input_commodity
    FOREIGN KEY (commodity_id)
    REFERENCES commodity(id)
    ON DELETE RESTRICT,
ADD CONSTRAINT fk_industry_input_industry
    FOREIGN KEY (industry_id)
    REFERENCES industry(id)
    ON DELETE CASCADE,
ADD CONSTRAINT chk_industry_input_amount_nonnegative
    CHECK (amount >= 0);

-- Industry output FKs + CHECK
ALTER TABLE industry_output
ADD CONSTRAINT fk_industry_output_commodity
    FOREIGN KEY (commodity_id)
    REFERENCES commodity(id)
    ON DELETE RESTRICT,
ADD CONSTRAINT fk_industry_output_industry
    FOREIGN KEY (industry_id)
    REFERENCES industry(id)
    ON DELETE CASCADE,
ADD CONSTRAINT chk_industry_output_amount_nonnegative
    CHECK (amount >= 0);

-- Industry track route (subclass of track_block)
ALTER TABLE industry_track_block
ADD CONSTRAINT fk_industry_track_block_track_block
    FOREIGN KEY (id)
    REFERENCES track_block(id)
    ON DELETE CASCADE,
ADD CONSTRAINT chk_industry_track_block_load_time_nonnegative
    CHECK (load_time_minutes IS NULL OR load_time_minutes >= 0);

-- Map: industry ↔ track_block (industry spurs)
ALTER TABLE industry_track_block_map
ADD CONSTRAINT fk_itr_map_industry
    FOREIGN KEY (industry_id)
    REFERENCES industry(id)
    ON DELETE CASCADE,
ADD CONSTRAINT fk_itr_map_track_block
    FOREIGN KEY (track_block_id)
    REFERENCES track_block(id)
    ON DELETE CASCADE;
