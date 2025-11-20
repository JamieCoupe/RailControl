-- ==========================================================
-- Trigger: each turnout must have at least two legs
-- ==========================================================

CREATE OR REPLACE FUNCTION enforce_turnout_leg_count()
RETURNS trigger AS $$
DECLARE
    t_id      VARCHAR(20);
    leg_count INT;
BEGIN
    t_id := COALESCE(NEW.turnout_id, OLD.turnout_id);

    SELECT COUNT(*) INTO leg_count
    FROM turnout_leg
    WHERE turnout_id = t_id;

    IF leg_count < 2 THEN
        RAISE EXCEPTION 'Turnout % must have at least 2 legs', t_id;
    END IF;

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_enforce_turnout_leg_count ON turnout_leg;

CREATE TRIGGER trg_enforce_turnout_leg_count
AFTER INSERT OR DELETE ON turnout_leg
FOR EACH ROW EXECUTE FUNCTION enforce_turnout_leg_count();

-- ==========================================================
-- Trigger: platform_track_route must match route_type = 'platform'
-- ==========================================================

CREATE OR REPLACE FUNCTION enforce_platform_track_route_type()
RETURNS trigger AS $$
DECLARE
    rt_type track_route_type_enum;
BEGIN
    SELECT route_type INTO rt_type
    FROM track_route
    WHERE id = NEW.id;

    IF rt_type IS NULL THEN
        RAISE EXCEPTION 'No track_route with id % exists for platform_track_route', NEW.id;
    ELSIF rt_type <> 'platform' THEN
        RAISE EXCEPTION 'Track route % must have route_type=platform for platform_track_route', NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_enforce_platform_track_route_type ON platform_track_route;

CREATE TRIGGER trg_enforce_platform_track_route_type
BEFORE INSERT OR UPDATE ON platform_track_route
FOR EACH ROW EXECUTE FUNCTION enforce_platform_track_route_type();

-- ==========================================================
-- Trigger: industry_track_route must match route_type = 'industry'
-- ==========================================================

CREATE OR REPLACE FUNCTION enforce_industry_track_route_type()
RETURNS trigger AS $$
DECLARE
    rt_type track_route_type_enum;
BEGIN
    SELECT route_type INTO rt_type
    FROM track_route
    WHERE id = NEW.id;

    IF rt_type IS NULL THEN
        RAISE EXCEPTION 'No track_route with id % exists for industry_track_route', NEW.id;
    ELSIF rt_type <> 'industry' THEN
        RAISE EXCEPTION 'Track route % must have route_type=industry for industry_track_route', NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_enforce_industry_track_route_type ON industry_track_route;

CREATE TRIGGER trg_enforce_industry_track_route_type
BEFORE INSERT OR UPDATE ON industry_track_route
FOR EACH ROW EXECUTE FUNCTION enforce_industry_track_route_type();
