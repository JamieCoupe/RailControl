-- ==========================================================
-- Constraints for stations module
-- ==========================================================

-- station.name must be unique
ALTER TABLE station
ADD CONSTRAINT uq_station_name UNIQUE (name);


-- station_track_route mapping should be unique
ALTER TABLE station_track_route
ADD CONSTRAINT uq_station_track_route_pair UNIQUE (station_id, track_route_id);


-- Ensure that each platform_track_route ID corresponds to a track_route
-- with route_type='platform'
-- This is enforced in triggers/triggers.sql

-- No partial index needed — remove old index entirely

-- Optional index to speed lookups
CREATE INDEX idx_station_track_route_station
    ON station_track_route(station_id);

CREATE INDEX idx_station_track_route_route
    ON station_track_route(track_route_id);
