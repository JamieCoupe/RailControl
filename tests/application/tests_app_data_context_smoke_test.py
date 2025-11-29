from src.application.app_context import AppDataContext

def write_yaml(path, text):
    path.write_text(text.strip() + "\n")


def test_app_context_builds_minimal(tmp_path):
    # Write tiny YAML files into tmp_path (same as repo provider test)
    write_yaml(tmp_path / "commodities.yml", """
    commodities:
      - id: COAL
        name: Coal
        unit: tons
        default_wagon_type: HOPPER
    """)

    write_yaml(tmp_path / "industries.yml", """
    industries:
      - id: IND_COAL
        name: Coal Mine
        industry_type: mine
        inputs: []
        outputs: []
    """)

    write_yaml(tmp_path / "track_blocks.yml", """
    track_blocks:
      - id: BLK_MAIN_1
        name: Mainline Section
        block_type: MAINLINE
        block_class: MAINLINE
    """)

    write_yaml(tmp_path / "track_sections.yml", """
    track_sections:
      - id: SEC_01
        block_id: BLK_MAIN_1
        start_junction_id: J1
        end_junction_id: J2
        length_mm: 1000
        max_speed: 80
    """)

    write_yaml(tmp_path / "turnouts.yml", """
    turnouts:
      - id: T01
        name: Test Turnout
        turnout_type: STANDARD_LEFT
        straight_section_id: SEC_01
        diverging_section_id: SEC_02
        current_state: STRAIGHT
    """)

    write_yaml(tmp_path / "stations.yml", """
    stations:
      - id: STN_A
        name: Example Station
    """)

    write_yaml(tmp_path /  "junctions.yml", """
    junctions:
      - junction_id: J1
        name: Test Junction
        junction_type: STANDARD
      - junction_id: J2
        name: Test Junction
        junction_type: STANDARD
    """)


    ctx = AppDataContext(str(tmp_path))

    assert ctx.repos is not None
    assert ctx.topology_builder is not None
    assert ctx.routing is not None