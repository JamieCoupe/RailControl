from src.domain.domain_enums import TrackBlockType
from src.domain.track.track_block import PlatformTrackBlock, TrackBlock, IndustryTrackBlock
from src.infrastructure.data_sources.yaml.track_block_loader import TrackBlockYamlLoader
from src.infrastructure.repository.track_block_repository import TrackBlockRepository


class YamlTrackBlockRepository(TrackBlockRepository):

    def __init__(self, loader: TrackBlockYamlLoader):
        raw = loader.load()

        self._track_blocks_by_id: dict[str, TrackBlock] = {}
        self._platform_blocks_by_id: dict[str, PlatformTrackBlock] = {}
        self._industry_blocks_by_id: dict[str, IndustryTrackBlock] = {}

        for raw_track_block in raw["track_blocks"]:
            if "station_id" in raw_track_block:
                platform_block = PlatformTrackBlock(
                    raw_track_block['id'],
                    raw_track_block['name'],
                    TrackBlockType[raw_track_block['block_type'].upper()],
                    raw_track_block['station_id'],
                    raw_track_block['dwell_time_minutes'],
                    raw_track_block['platform_number'],
                )
                self._platform_blocks_by_id[raw_track_block['id']] = platform_block
                track_block = platform_block

            elif "industry_id" in raw_track_block:
                industry_block = IndustryTrackBlock(
                    raw_track_block['id'],
                    raw_track_block['name'],
                    TrackBlockType[raw_track_block['block_type'].upper()],
                    raw_track_block['industry_id'],
                    raw_track_block['load_time_minutes'],
                )
                self._industry_blocks_by_id[raw_track_block['id']] = industry_block
                track_block = industry_block
            else:
                track_block = TrackBlock(
                    raw_track_block['id'],
                    raw_track_block['name'],
                    TrackBlockType[raw_track_block['block_type'].upper()],
                )
            self._track_blocks_by_id[raw_track_block['id']] = track_block

    def get(self, track_block_id: str) -> TrackBlock:
        return self._track_blocks_by_id[track_block_id]

    def get_by_station(self, station_id) -> list[PlatformTrackBlock] | None:
        return list(platform_block for platform_block in self._platform_blocks_by_id.values() if platform_block.station_id == station_id)

    def get_by_industry(self, industry_id) -> list[IndustryTrackBlock] | None:
        return list(industry_block for industry_block in self._industry_blocks_by_id.values() if industry_block.industry_id == industry_id)

    def get_all(self) -> list[TrackBlock]:
        return list(self._track_blocks_by_id.values())

    def get_all_platform_blocks(self) -> list[PlatformTrackBlock]:
        return list(self._platform_blocks_by_id.values())

    def get_all_industry_blocks(self) -> list[IndustryTrackBlock]:
        return list(self._industry_blocks_by_id.values())

