from railcontrol.domain.track.track_block import TrackBlock


class Station:
    def __init__(self, id: str, name: str, track_blocks: list[TrackBlock]):
        self.id = id
        self.name = name
        self.track_blocks = track_blocks