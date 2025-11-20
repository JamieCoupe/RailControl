-- ==========================================================
-- Track constraints
-- ==========================================================

-- Non-negative lengths
ALTER TABLE track_section
    ADD CONSTRAINT chk_track_section_length_nonnegative
    CHECK (length_mm >= 0);

-- Either both junctions null (loose end), or both non-null and different
ALTER TABLE track_section
    ADD CONSTRAINT chk_track_section_junctions
    CHECK (
        (start_junction_id IS NULL AND end_junction_id IS NULL)
        OR
        (start_junction_id IS NOT NULL AND end_junction_id IS NOT NULL
         AND start_junction_id <> end_junction_id)
    );

-- Positive sequence number in a route
ALTER TABLE track_route_track_section
    ADD CONSTRAINT chk_trts_sequence_positive
    CHECK (sequence >= 1);

-- Only one leg of each type per turnout (you already had this)
CREATE UNIQUE INDEX idx_unique_turnout_leg_type
ON turnout_leg(turnout_id, leg_type);

-- At most one row per (route, sequence)
CREATE UNIQUE INDEX idx_trts_sequence_per_route
ON track_route_track_section(track_route_id, sequence);
