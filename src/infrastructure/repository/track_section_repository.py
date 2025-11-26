from src.domain.track.track_section import TrackSection

class TrackSectionRepository:
    def get(self, track_section_id: str) -> TrackSection:
        raise NotImplementedError
    def get_all(self) -> list[TrackSection]:
        raise NotImplementedError
    def get_by_block_id(self, block_id) -> list[TrackSection]:
        raise NotImplementedError