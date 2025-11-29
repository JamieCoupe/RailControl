from railcontrol.domain.timetable.timetable import Timetable

class TimetableRepositry:
    def get(self, wagon_id: str) -> Timetable:
        raise NotImplementedError
    def list_all(self) -> list[Timetable]:
        raise NotImplementedError
