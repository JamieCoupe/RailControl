from src.domain.track.track_block import TrackBlock
from src.domain.track.track_block import PlatformTrackBlock
from src.domain.track.track_block import IndustryTrackBlock

class TrackBlockRepository:
    def get(self, track_block_id: str) -> TrackBlock:
        raise NotImplementedError

    def get_all(self) -> list[TrackBlock]:
        raise NotImplementedError

    def get_all_platform_blocks(self) -> list[PlatformTrackBlock]:
        raise NotImplementedError

    def get_all_industry_blocks(self) -> list[IndustryTrackBlock]:
        raise NotImplementedError
