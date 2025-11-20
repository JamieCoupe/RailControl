INSERT INTO commodity VALUES
    ('COM_FUEL', 'Diesel Fuel', 'litres', NULL),
    ('COM_AVGAS', 'Aviation Gasoline', 'litres', NULL);

INSERT INTO wagon_classification VALUES
    ('WCL_TEA', 'TEA', 'tanker', 15200),
    ('WCL_TANK_SMALL', 'TKA', 'tanker', 11000),
    ('WCL_HOP', 'HOP', 'hopper', 9800),
    ('WCL_COAL', 'COA', 'open', 10200),
    ('WCL_CONT', 'CON', 'container_flat', 13800);

INSERT INTO wagon_compatible_commodity VALUES
    ('WCC_001', 'COM_FUEL', 'WCL_TEA'),
    ('WCC_002', 'COM_FUEL', 'WCL_TANK_SMALL'),
    ('WCC_003', 'COM_AVGAS', 'WCL_TEA');

INSERT INTO wagon VALUES
    ('W1', 'VTG 30001', 'WCL_TEA', 100000),
    ('W2', 'VTG 30002', 'WCL_TEA', 100000),
    ('W3', 'VTG 30003', 'WCL_TANK_SMALL', 60000),
    ('W4', 'EWS 12001', 'WCL_COAL', 45000),
    ('W5', 'EWS 12055', 'WCL_CONT', 52000);

INSERT INTO industry VALUES
    ('IND_KFT', 'Kilnside Fuel Terminal', 'terminal');

INSERT INTO industry_input VALUES
    ('COM_FUEL', 'IND_KFT', 300000);

INSERT INTO industry_output VALUES
    ('COM_FUEL', 'IND_KFT', 0);

INSERT INTO station VALUES
    ('STA_KILN', 'Kilnside');

INSERT INTO track_route VALUES
    ('TR_MAIN_1', 'Main Through Line', 'mainline'),
    ('TR_PF1', 'Kilnside Platform 1', 'platform'),
    ('TR_PF2', 'Kilnside Platform 2', 'platform'),

    ('TR_SPUR', 'Fuel Terminal Spur', 'industry'),
    ('TR_IND_AD1', 'Fuel Terminal Arr/Dep 1', 'industry'),
    ('TR_IND_AD2', 'Fuel Terminal Arr/Dep 2', 'industry'),
    ('TR_IND_LOAD', 'Fuel Terminal Loading Siding', 'industry'),
    ('TR_IND_HS', 'Fuel Terminal Headshunt', 'industry');

INSERT INTO platform_track_route VALUES
    ('TR_PF1', 1, 60),
    ('TR_PF2', 2, 60);

INSERT INTO industry_track_route (id, load_time_minutes) VALUES
    ('TR_SPUR', 0),
    ('TR_IND_AD1', 8),
    ('TR_IND_AD2', 8),
    ('TR_IND_LOAD', 20),
    ('TR_IND_HS', 0);

INSERT INTO industry_track_route_map (industry_id, track_route_id) VALUES
('IND_KFT', 'TR_SPUR'),
('IND_KFT', 'TR_IND_AD1'),
('IND_KFT', 'TR_IND_AD2'),
('IND_KFT', 'TR_IND_LOAD'),
('IND_KFT', 'TR_IND_HS');

INSERT INTO station_track_route VALUES
    ('STA_KILN', 'TR_MAIN_1'),
    ('STA_KILN', 'TR_PF1'),
    ('STA_KILN', 'TR_PF2');

INSERT INTO track_route VALUES
('TR_UP_PLATFORM', 'Up Platform', 'platform'),
('TR_DN_PLATFORM', 'Down Platform', 'platform'),
('TR_THROUGH', 'Through Road', 'mainline'),
('TR_SPUR', 'Kilnside Fuel Spur', 'industry'),
('TR_AD1', 'Terminal Arrival 1', 'industry'),
('TR_AD2', 'Terminal Arrival 2', 'industry'),
('TR_LOAD', 'Terminal Load/Unload', 'industry'),
('TR_IND_HS', 'Industry Headshunt', 'headshunt'),
('TR_SPUR_HS', 'Spur Headshunt', 'headshunt');

INSERT INTO junction VALUES
('JCT_TR_UP_PLATFORM_1A',  'Up Plat J1A', 'plain', 10),
('JCT_TR_UP_PLATFORM_1B',  'Up Plat J1B', 'plain', 10),
('JCT_TR_UP_PLATFORM_2A',  'Up Plat J2A', 'plain', 10),
('JCT_TR_UP_PLATFORM_2B',  'Up Plat J2B', 'plain', 10),
('JCT_TR_UP_PLATFORM_3A',  'Up Plat J3A', 'plain', 10),
('JCT_TR_UP_PLATFORM_3B',  'Up Plat J3B', 'plain', 10),

('JCT_TR_DN_PLATFORM_1A', 'Dn Plat J1A', 'plain', 10),
('JCT_TR_DN_PLATFORM_1B', 'Dn Plat J1B', 'plain', 10),
('JCT_TR_DN_PLATFORM_2A', 'Dn Plat J2A', 'plain', 10),
('JCT_TR_DN_PLATFORM_2B', 'Dn Plat J2B', 'plain', 10),
('JCT_TR_DN_PLATFORM_3A', 'Dn Plat J3A', 'plain', 10),
('JCT_TR_DN_PLATFORM_3B', 'Dn Plat J3B', 'plain', 10),

('JCT_TR_THROUGH_1A', 'Through J1A', 'plain', 10),
('JCT_TR_THROUGH_1B', 'Through J1B', 'plain', 10),
('JCT_TR_THROUGH_2A', 'Through J2A', 'plain', 10),
('JCT_TR_THROUGH_2B', 'Through J2B', 'plain', 10),
('JCT_TR_THROUGH_3A', 'Through J3A', 'plain', 10),
('JCT_TR_THROUGH_3B', 'Through J3B', 'plain', 10),

('JCT_TR_SPUR_1A', 'Spur J1A', 'plain', 10),
('JCT_TR_SPUR_1B', 'Spur J1B', 'plain', 10),
('JCT_TR_SPUR_2A', 'Spur J2A', 'plain', 10),
('JCT_TR_SPUR_2B', 'Spur J2B', 'plain', 10),
('JCT_TR_SPUR_3A', 'Spur J3A', 'plain', 10),
('JCT_TR_SPUR_3B', 'Spur J3B', 'plain', 10),

('JCT_TR_AD1_1A', 'AD1 J1A', 'plain', 10),
('JCT_TR_AD1_1B', 'AD1 J1B', 'plain', 10),
('JCT_TR_AD1_2A', 'AD1 J2A', 'plain', 10),
('JCT_TR_AD1_2B', 'AD1 J2B', 'plain', 10),
('JCT_TR_AD1_3A', 'AD1 J3A', 'plain', 10),
('JCT_TR_AD1_3B', 'AD1 J3B', 'plain', 10),

('JCT_TR_AD2_1A', 'AD2 J1A', 'plain', 10),
('JCT_TR_AD2_1B', 'AD2 J1B', 'plain', 10),
('JCT_TR_AD2_2A', 'AD2 J2A', 'plain', 10),
('JCT_TR_AD2_2B', 'AD2 J2B', 'plain', 10),
('JCT_TR_AD2_3A', 'AD2 J3A', 'plain', 10),
('JCT_TR_AD2_3B', 'AD2 J3B', 'plain', 10),

('JCT_TR_LOAD_1A', 'Load J1A', 'plain', 10),
('JCT_TR_LOAD_1B', 'Load J1B', 'plain', 10),
('JCT_TR_LOAD_2A', 'Load J2A', 'plain', 10),
('JCT_TR_LOAD_2B', 'Load J2B', 'plain', 10),
('JCT_TR_LOAD_3A', 'Load J3A', 'plain', 10),
('JCT_TR_LOAD_3B', 'Load J3B', 'plain', 10),

('JCT_TR_IND_HS_1A', 'Ind HS J1A', 'buffer', 10),
('JCT_TR_IND_HS_1B', 'Ind HS J1B', 'plain', 10),

('JCT_TR_SPUR_HS_1A', 'Spur HS J1A', 'buffer', 10),
('JCT_TR_SPUR_HS_1B', 'Spur HS J1B', 'plain', 10);

INSERT INTO track_section VALUES
('TS_UP_1', 'Up Platform Sec 1', 500, 'JCT_TR_UP_PLATFORM_1A', 'JCT_TR_UP_PLATFORM_1B', 'platform', NULL),
('TS_UP_2', 'Up Platform Sec 2', 500, 'JCT_TR_UP_PLATFORM_2A', 'JCT_TR_UP_PLATFORM_2B', 'platform', NULL),
('TS_UP_3', 'Up Platform Sec 3', 500, 'JCT_TR_UP_PLATFORM_3A', 'JCT_TR_UP_PLATFORM_3B', 'platform', NULL),

('TS_DN_1', 'Down Platform Sec 1', 500, 'JCT_TR_DN_PLATFORM_1A', 'JCT_TR_DN_PLATFORM_1B', 'platform', NULL),
('TS_DN_2', 'Down Platform Sec 2', 500, 'JCT_TR_DN_PLATFORM_2A', 'JCT_TR_DN_PLATFORM_2B', 'platform', NULL),
('TS_DN_3', 'Down Platform Sec 3', 500, 'JCT_TR_DN_PLATFORM_3A', 'JCT_TR_DN_PLATFORM_3B', 'platform', NULL),

('TS_TH_1', 'Through Sec 1', 500, 'JCT_TR_THROUGH_1A', 'JCT_TR_THROUGH_1B', 'mainline', NULL),
('TS_TH_2', 'Through Sec 2', 500, 'JCT_TR_THROUGH_2A', 'JCT_TR_THROUGH_2B', 'mainline', NULL),
('TS_TH_3', 'Through Sec 3', 500, 'JCT_TR_THROUGH_3A', 'JCT_TR_THROUGH_3B', 'mainline', NULL),

('TS_SPUR_1', 'Spur Sec 1', 500, 'JCT_TR_SPUR_1A', 'JCT_TR_SPUR_1B', 'industry_spur', NULL),
('TS_SPUR_2', 'Spur Sec 2', 500, 'JCT_TR_SPUR_2A', 'JCT_TR_SPUR_2B', 'industry_spur', NULL),
('TS_SPUR_3', 'Spur Sec 3', 500, 'JCT_TR_SPUR_3A', 'JCT_TR_SPUR_3B', 'industry_spur', NULL),

('TS_AD1_1', 'Arrival 1 Sec 1', 500, 'JCT_TR_AD1_1A', 'JCT_TR_AD1_1B', 'industry_loading', NULL),
('TS_AD1_2', 'Arrival 1 Sec 2', 500, 'JCT_TR_AD1_2A', 'JCT_TR_AD1_2B', 'industry_loading', NULL),
('TS_AD1_3', 'Arrival 1 Sec 3', 500, 'JCT_TR_AD1_3A', 'JCT_TR_AD1_3B', 'industry_loading', NULL),

('TS_AD2_1', 'Arrival 2 Sec 1', 500, 'JCT_TR_AD2_1A', 'JCT_TR_AD2_1B', 'industry_loading', NULL),
('TS_AD2_2', 'Arrival 2 Sec 2', 500, 'JCT_TR_AD2_2A', 'JCT_TR_AD2_2B', 'industry_loading', NULL),
('TS_AD2_3', 'Arrival 2 Sec 3', 500, 'JCT_TR_AD2_3A', 'JCT_TR_AD2_3B', 'industry_loading', NULL),

('TS_LOAD_1', 'Load Line Sec 1', 500, 'JCT_TR_LOAD_1A', 'JCT_TR_LOAD_1B', 'industry_loading', NULL),
('TS_LOAD_2', 'Load Line Sec 2', 500, 'JCT_TR_LOAD_2A', 'JCT_TR_LOAD_2B', 'industry_loading', NULL),
('TS_LOAD_3', 'Load Line Sec 3', 500, 'JCT_TR_LOAD_3A', 'JCT_TR_LOAD_3B', 'industry_loading', NULL),

('TS_INDHS_1', 'Industry HS', 500, 'JCT_TR_IND_HS_1A', 'JCT_TR_IND_HS_1B', 'headshunt', NULL),

('TS_SPURHS_1', 'Spur HS', 500, 'JCT_TR_SPUR_HS_1A', 'JCT_TR_SPUR_HS_1B', 'headshunt', NULL);

INSERT INTO track_route_track_section VALUES
('TR_UP_PLATFORM_01', 'TR_UP_PLATFORM', 'TS_UP_1', 1, 'forward'),
('TR_UP_PLATFORM_02', 'TR_UP_PLATFORM', 'TS_UP_2', 2, 'forward'),
('TR_UP_PLATFORM_03', 'TR_UP_PLATFORM', 'TS_UP_3', 3, 'forward'),

('TR_DN_PLATFORM_01', 'TR_DN_PLATFORM', 'TS_DN_1', 1, 'forward'),
('TR_DN_PLATFORM_02', 'TR_DN_PLATFORM', 'TS_DN_2', 2, 'forward'),
('TR_DN_PLATFORM_03', 'TR_DN_PLATFORM', 'TS_DN_3', 3, 'forward'),

('TR_THROUGH_01', 'TR_THROUGH', 'TS_TH_1', 1, 'forward'),
('TR_THROUGH_02', 'TR_THROUGH', 'TS_TH_2', 2, 'forward'),
('TR_THROUGH_03', 'TR_THROUGH', 'TS_TH_3', 3, 'forward'),

('TR_SPUR_01', 'TR_SPUR', 'TS_SPUR_1', 1, 'forward'),
('TR_SPUR_02', 'TR_SPUR', 'TS_SPUR_2', 2, 'forward'),
('TR_SPUR_03', 'TR_SPUR', 'TS_SPUR_3', 3, 'forward'),

('TR_AD1_01', 'TR_AD1', 'TS_AD1_1', 1, 'forward'),
('TR_AD1_02', 'TR_AD1', 'TS_AD1_2', 2, 'forward'),
('TR_AD1_03', 'TR_AD1', 'TS_AD1_3', 3, 'forward'),

('TR_AD2_01', 'TR_AD2', 'TS_AD2_1', 1, 'forward'),
('TR_AD2_02', 'TR_AD2', 'TS_AD2_2', 2, 'forward'),
('TR_AD2_03', 'TR_AD2', 'TS_AD2_3', 3, 'forward'),

('TR_LOAD_01', 'TR_LOAD', 'TS_LOAD_1', 1, 'forward'),
('TR_LOAD_02', 'TR_LOAD', 'TS_LOAD_2', 2, 'forward'),
('TR_LOAD_03', 'TR_LOAD', 'TS_LOAD_3', 3, 'forward'),

('TR_INDHS_01', 'TR_IND_HS', 'TS_INDHS_1', 1, 'forward'),

('TR_SPURHS_01', 'TR_SPUR_HS', 'TS_SPURHS_1', 1, 'forward');

INSERT INTO platform_track_route VALUES
('TR_UP_PLATFORM', 1, 2),
('TR_DN_PLATFORM', 2, 2);

INSERT INTO industry_track_route_map VALUES
('TR_SPUR', 'IND_KFT'),
('TR_AD1', 'IND_KFT'),
('TR_AD2', 'IND_KFT'),
('TR_LOAD', 'IND_KFT'),
('TR_IND_HS', 'IND_KFT');

-- ----------------------------------------------------------
-- TURNOUTS
-- ----------------------------------------------------------

-- === UP PLATFORM turnouts ===
INSERT INTO turnout (id, junction_id, name) VALUES
('TO_UP', 'JCT_TR_UP_PLATFORM_2A', 'TO Up Platform');

INSERT INTO turnout_leg (turnout_id, track_section_id, leg_type) VALUES
('TO_UP', 'TS_UP_2', 'straight'),
('TO_UP', 'TS_UP_3', 'diverging');


-- === DOWN PLATFORM ===
INSERT INTO turnout (id, junction_id, name) VALUES
('TO_DN', 'JCT_TR_DN_PLATFORM_2A', 'TO Down Platform');

INSERT INTO turnout_leg VALUES
('TO_DN', 'TS_DN_2', 'straight'),
('TO_DN', 'TS_DN_3', 'diverging');


-- === THROUGH ROAD ===
INSERT INTO turnout VALUES
('TO_TH', 'JCT_TR_THROUGH_2A', 'TO Through Road');

INSERT INTO turnout_leg VALUES
('TO_TH', 'TS_TH_2', 'straight'),
('TO_TH', 'TS_TH_3', 'diverging');


-- === SPUR LEAD ===
INSERT INTO turnout VALUES
('TO_SPUR', 'JCT_TR_SPUR_2A', 'TO Spur Lead');

INSERT INTO turnout_leg VALUES
('TO_SPUR', 'TS_SPUR_2', 'straight'),
('TO_SPUR', 'TS_SPUR_3', 'diverging');


-- === INDUSTRY ARRIVAL 1 (AD1) ===
INSERT INTO turnout VALUES
('TO_AD1', 'JCT_TR_AD1_2A', 'TO Industry Arrival 1');

INSERT INTO turnout_leg VALUES
('TO_AD1', 'TS_AD1_2', 'straight'),
('TO_AD1', 'TS_AD1_3', 'diverging');


-- === INDUSTRY ARRIVAL 2 (AD2) ===
INSERT INTO turnout VALUES
('TO_AD2', 'JCT_TR_AD2_2A', 'TO Industry Arrival 2');

INSERT INTO turnout_leg VALUES
('TO_AD2', 'TS_AD2_2', 'straight'),
('TO_AD2', 'TS_AD2_3', 'diverging');


-- === LOAD / UNLOAD LINE ===
INSERT INTO turnout VALUES
('TO_LOAD', 'JCT_TR_LOAD_2A', 'TO Load/Unload');

INSERT INTO turnout_leg VALUES
('TO_LOAD', 'TS_LOAD_2', 'straight'),
('TO_LOAD', 'TS_LOAD_3', 'diverging');


-- ----------------------------------------------------------
-- BUFFERS
-- ----------------------------------------------------------
-- Buffers = junctions of type 'buffer'
-- Headshunts and dead ends get buffer junctions.
-- ----------------------------------------------------------

-- === INDUSTRY HEADSHUNT (east) ===
INSERT INTO junction (id, name, junction_type, length_mm) VALUES
('JCT_IND_HS_BUF', 'Industry Headshunt Buffer', 'buffer', 0);

-- Attach to track_section TS_IND_HS_1
UPDATE track_section
SET end_junction_id = 'JCT_IND_HS_BUF'
WHERE id = 'TS_IND_HS_1';


-- === SPUR HEADSHUNT (west) ===
INSERT INTO junction (id, name, junction_type, length_mm) VALUES
('JCT_SPUR_HS_BUF', 'Spur Headshunt Buffer', 'buffer', 0);

UPDATE track_section
SET end_junction_id = 'JCT_SPUR_HS_BUF'
WHERE id = 'TS_SPUR_HS_1';


-- === TERMINAL ARRIVAL 1 STOP (AD1 STOP section) ===
INSERT INTO junction VALUES
('JCT_AD1_BUF', 'Arrival 1 Buffer', 'buffer', 0);

UPDATE track_section
SET end_junction_id = 'JCT_AD1_BUF'
WHERE id = 'TS_AD1_3';


-- === TERMINAL ARRIVAL 2 STOP (AD2 STOP section) ===
INSERT INTO junction VALUES
('JCT_AD2_BUF', 'Arrival 2 Buffer', 'buffer', 0);

UPDATE track_section
SET end_junction_id = 'JCT_AD2_BUF'
WHERE id = 'TS_AD2_3';


-- === LOAD/UNLOAD Siding Buffer ===
INSERT INTO junction VALUES
('JCT_LOAD_BUF', 'Loading Siding Buffer', 'buffer', 0);

UPDATE track_section
SET end_junction_id = 'JCT_LOAD_BUF'
WHERE id = 'TS_LOAD_3';