import pytest
import os

from src.infrastructure.providers.repository_provider import RepositoryProvider


def write_yaml(path, text):
    path.write_text(text.strip() + "\n")


def test_repository_provider_builds_all_repos(tmp_path):
    """
    Smoke test: ensures RepositoryProvider successfully builds
    all repositories when valid YAML files exist.
    """

    # -------- Arrange: create minimal valid YAML files --------
    write_yaml(tmp_path / "commodities.yaml", """
    commodities:
      - id: COAL
        name: Coal
        unit: tons
        default_wagon_type: HOPPER
    """)

    write_yaml(tmp_path / "industries.yaml", """
    industries:
      - id: IND_COAL
        name: Coal Mine
        industry_type: mine
        inputs: []
        outputs: []
    """)

    write_yaml(tmp_path / "track_blocks.yaml", """
    track_blocks:
      - id: BLK_MAIN_1
        name: Mainline Section
        block_type: MAINLINE
    """)

    write_yaml(tmp_path / "track_sections.yaml", """
    track_sections:
      - id: SEC_01
        block_id: BLK_MAIN_1
        start_junction_id: J1
        end_junction_id: J2
        length_mm: 1000
        max_speed: 80
    """)

    write_yaml(tmp_path / "turnouts.yaml", """
    turnouts:
      - id: T01
        name: Test Turnout
        turnout_type: STANDARD_LEFT
        straight_section_id: SEC_01
        diverging_section_id: SEC_01
        current_state: STRAIGHT
    """)

    write_yaml(tmp_path / "stations.yaml", """
    stations:
      - id: STN_A
        name: Example Station
    """)

    write_yaml(tmp_path /  "junctions.yaml", """
    junctions:
      - id: J1
        name: Test Junction
        type: plain
    """)

    # -------- Act --------
    provider = RepositoryProvider(str(tmp_path))

    # -------- Assert: ensure each repository exists and loads correctly --------
    assert provider.commodities is not None
    assert provider.industries is not None
    assert provider.track_blocks is not None
    assert provider.track_sections is not None
    assert provider.turnouts is not None
    assert provider.stations is not None

    # Quick internal checks
    assert provider.commodities.get("COAL").name == "Coal"
    assert provider.track_sections.get("SEC_01").length_mm == 1000
    assert provider.industries.get("IND_COAL").name == "Coal Mine"
    assert provider.stations.get("STN_A").name == "Example Station"

def test_repository_provider_raises_on_missing_yaml(tmp_path):
    # No YAML files created!
    with pytest.raises(Exception):
        RepositoryProvider(str(tmp_path))