from railcontrol.domain.timetable.train_service import TrainService

class TrainServiceRepositry:
    def get(self, wagon_id: str) -> TrainService:
        raise NotImplementedError
    def list_all(self) -> list[TrainService]:
        raise NotImplementedError
