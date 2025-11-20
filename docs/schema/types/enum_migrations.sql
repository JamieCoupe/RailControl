
-- ==========================================================
-- Apply enums to existing columns
-- ==========================================================

ALTER TABLE wagon_classification
    ALTER COLUMN wagon_type TYPE wagon_type_enum
    USING wagon_type::wagon_type_enum;

ALTER TABLE junction
    ALTER COLUMN junction_type TYPE junction_type_enum
    USING junction_type::junction_type_enum;

ALTER TABLE track_route
    ALTER COLUMN route_type TYPE track_route_type_enum
    USING route_type::track_route_type_enum;

ALTER TABLE track_section
    ALTER COLUMN track_type TYPE track_section_type_enum
    USING track_type::track_section_type_enum;

ALTER TABLE track_route_track_section
    ALTER COLUMN direction TYPE direction_enum
    USING direction::direction_enum;

ALTER TABLE turnout_leg
    ALTER COLUMN leg_type TYPE turnout_leg_enum
    USING leg_type::turnout_leg_enum;

ALTER TABLE industry
    ALTER COLUMN type TYPE industry_type_enum
    USING type::industry_type_enum;
