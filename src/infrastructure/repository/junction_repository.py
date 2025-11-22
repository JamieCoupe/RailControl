from src.domain.track.junction import Junction

class JunctionRepository:
    def get(self, junction_id: str) -> Junction:
        raise NotImplementedError
    def get_all(self) -> list[Junction]:
        raise NotImplementedError
