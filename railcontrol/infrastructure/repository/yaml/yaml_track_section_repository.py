
from railcontrol.domain.track.track_section import TrackSection
from railcontrol.infrastructure.repository.track_section_repository import TrackSectionRepository
from railcontrol.infrastructure.data_sources.yaml.track_section_loader import TrackSectionYamlLoader


class YamlTrackSectionRepository(TrackSectionRepository):

    def __init__(self, loader: TrackSectionYamlLoader):
        raw = loader.load()

        self._track_sections: dict [str, TrackSection] = {}

        for raw_track_section in raw["track_sections"]:
            track_section = TrackSection(
                raw_track_section['id'],
                raw_track_section['block_id'],
                raw_track_section['start_junction_id'],
                raw_track_section['end_junction_id'],
                raw_track_section['length_mm'],
                raw_track_section['max_speed'],
                )
            self._track_sections[raw_track_section['id']] = track_section

    def get(self, track_section_id: str) -> TrackSection:
        return self._track_sections[track_section_id]

    def get_all(self) -> list[TrackSection]:
        return list(self._track_sections.values())

    def get_by_block_id(self, block_id) -> list[TrackSection]:
        return list(track_section for track_section in self._track_sections.values() if track_section.block_id == block_id  )