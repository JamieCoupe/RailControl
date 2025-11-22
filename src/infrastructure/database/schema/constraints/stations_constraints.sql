-- ==========================================================
-- Constraints for stations module
-- ==========================================================

-- station.name must be unique
ALTER TABLE station
ADD CONSTRAINT uq_station_name UNIQUE (name);


-- station_track_block mapping should be unique
ALTER TABLE station_track_block
ADD CONSTRAINT uq_station_track_block_pair UNIQUE (station_id, track_block_id);


-- Ensure that each platform_track_block ID corresponds to a track_block
-- with route_type='platform'
-- This is enforced in triggers/triggers.sql

-- No partial index needed — remove old index entirely

-- Optional index to speed lookups
CREATE INDEX idx_station_track_block_station
    ON station_track_block(station_id);

CREATE INDEX idx_station_track_block_route
    ON station_track_block(track_block_id);
