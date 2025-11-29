-- Uniques from your existing file
ALTER TABLE wagon
ADD CONSTRAINT uq_wagon_running_number UNIQUE (running_number);

ALTER TABLE wagon_classification
ADD CONSTRAINT uq_wagon_classification_code UNIQUE (classification_code);

-- Non-negatives / FKs

ALTER TABLE wagon_classification
ADD CONSTRAINT chk_wagon_classification_length_positive
    CHECK (length_mm > 0);

ALTER TABLE wagon
ADD CONSTRAINT fk_wagon_classification
    FOREIGN KEY (wagon_classification_id)
    REFERENCES wagon_classification(id)
    ON DELETE RESTRICT,
ADD CONSTRAINT chk_wagon_capacity_nonnegative
    CHECK (capacity >= 0);

ALTER TABLE wagon_compatible_commodity
ADD CONSTRAINT fk_wcc_commodity
    FOREIGN KEY (commodity_id)
    REFERENCES commodity(id)
    ON DELETE RESTRICT,
ADD CONSTRAINT fk_wcc_wagon_classification
    FOREIGN KEY (wagon_classification_id)
    REFERENCES wagon_classification(id)
    ON DELETE RESTRICT;
