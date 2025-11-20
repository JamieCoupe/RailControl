-- ==========================================================
-- Unique route name
-- ==========================================================
ALTER TABLE track_route
ADD CONSTRAINT uq_track_route_name UNIQUE (name);


-- ==========================================================
-- Unique industry spur route per industry
--
-- Instead of using a subquery:
--   WHERE track_route.route_type = 'industry'
-- We enforce this by:
--   1. Checking it via trigger
--   2. Preventing duplicates with a simple unique index
-- ==========================================================

-- Only one industry_track_route may map to the same industry+route combination
ALTER TABLE industry_track_route_map
ADD CONSTRAINT uq_industry_track_route UNIQUE (industry_id, track_route_id);


-- ==========================================================
-- Unique platform_track_route.id constraint
--	(platform routes map 1:1 to track_route)
-- ==========================================================
ALTER TABLE platform_track_route
ADD CONSTRAINT uq_platform_track_route UNIQUE (id);


-- ==========================================================
-- Route/section mapping FKs (OK AS-IS)
-- ==========================================================

ALTER TABLE track_route_track_section
ADD CONSTRAINT fk_trts_track_route
    FOREIGN KEY (track_route_id)
    REFERENCES track_route(id)
    ON DELETE CASCADE,
ADD CONSTRAINT fk_trts_track_section
    FOREIGN KEY (track_section_id)
    REFERENCES track_section(id)
    ON DELETE RESTRICT;

