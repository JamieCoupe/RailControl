from railcontrol.domain.domain_enums import TrackBlockType, TrackBlockClass


class TrackBlock:
    def __init__(
            self,
            id: str,
            name:str,
            track_block_type: TrackBlockType,
            track_block_class: TrackBlockClass
        ):
        self.id = id
        self.name = name
        self.track_block_type = track_block_type
        self.track_block_class = track_block_class

class PlatformTrackBlock(TrackBlock):
    def __init__(
            self,
            id: str,
            name:str,
            track_block_type: TrackBlockType,
            track_block_class: TrackBlockClass,
            station_id: str,
            dwell_time_minutes: int,
            platform_number: int
        ):
        super().__init__(id, name, track_block_type, track_block_class)
        self.station_id = station_id
        self.dwell_time_minutes = dwell_time_minutes
        self.platform_number = platform_number

class IndustryTrackBlock(TrackBlock):
    def __init__(
            self,
            id : str,
            name:str,
            track_block_type: TrackBlockType,
            track_block_class: TrackBlockClass,
            industry_id: str,
            load_time_minutes: int
        ):
        super().__init__(id, name, track_block_type, track_block_class)
        self.industry_id = industry_id
        self.load_time_minutes = load_time_minutes
