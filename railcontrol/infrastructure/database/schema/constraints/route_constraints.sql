-- ==========================================================
-- Unique route name
-- ==========================================================
ALTER TABLE track_block
ADD CONSTRAINT uq_track_block_name UNIQUE (name);


-- ==========================================================
-- Unique industry spur route per industry
--
-- Instead of using a subquery:
--   WHERE track_block.route_type = 'industry'
-- We enforce this by:
--   1. Checking it via trigger
--   2. Preventing duplicates with a simple unique index
-- ==========================================================

-- Only one industry_track_block may map to the same industry+route combination
ALTER TABLE industry_track_block_map
ADD CONSTRAINT uq_industry_track_block UNIQUE (industry_id, track_block_id);


-- ==========================================================
-- Unique platform_track_block.id constraint
--	(platform routes map 1:1 to track_block)
-- ==========================================================
ALTER TABLE platform_track_block
ADD CONSTRAINT uq_platform_track_block UNIQUE (id);


-- ==========================================================
-- Route/section mapping FKs (OK AS-IS)
-- ==========================================================

ALTER TABLE track_block_track_section
ADD CONSTRAINT fk_trts_track_block
    FOREIGN KEY (track_block_id)
    REFERENCES track_block(id)
    ON DELETE CASCADE,
ADD CONSTRAINT fk_trts_track_section
    FOREIGN KEY (track_section_id)
    REFERENCES track_section(id)
    ON DELETE RESTRICT;

