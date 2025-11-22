-- ==========================================================
-- Enum Types
-- ==========================================================

-- Wagon body / usage type
CREATE TYPE wagon_type_enum AS ENUM (
    'open',
    'hopper',
    'flat',
    'container_flat',
    'tanker'
);

-- Junction classification
CREATE TYPE junction_type_enum AS ENUM (
    'plain',
    'turnout',
    'crossing',
    'buffer'
);

-- Logical route type
CREATE TYPE track_block_type_enum AS ENUM (
    'mainline',
    'platform',
    'industry',
    'siding',
    'loop',
    'branch',
    'headshunt',
    'shed'
);

-- Physical track section type
CREATE TYPE track_section_type_enum AS ENUM (
    'mainline',
    'platform',
    'passing_loop',
    'siding',
    'headshunt',
    'industry_spur',
    'industry_loading',
    'shed'
);

-- Direction of a route over a section
CREATE TYPE direction_enum AS ENUM ('forward', 'reverse');

-- Turnout leg flavour
CREATE TYPE turnout_leg_enum AS ENUM ('straight', 'diverging');

-- Industry category
CREATE TYPE industry_type_enum AS ENUM (
    'factory',
    'mine',
    'terminal',
    'distribution'
);
