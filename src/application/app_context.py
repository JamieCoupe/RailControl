import logging

from src.application.routing.routing_service import RoutingService
from src.application.topology.topology_builder import TopologyBuilder
from src.infrastructure.providers.repository_provider import RepositoryProvider

logger = logging.getLogger(__name__)

class AppDataContext:

    def __init__(self, data_path: str):
        """
        The application-wide context.
        Builds repositories, services, engines, and exposes them.
        """
        logger.info(f"Starting App Context from: {data_path}")

        #Build repository provider
        self.repos = RepositoryProvider(data_path)

        #Build the topology builder
        self.topology_builder = TopologyBuilder(
            junction_repository=self.repos.junctions,          # not created yet
            track_section_repository=self.repos.track_sections,
            track_block_repository=self.repos.track_blocks,
            turnout_repository=self.repos.turnouts,
        )

        #Build the routing service
        routing_graph = self.topology_builder.build_graph()

        self.routing = RoutingService(routing_graph)

        # -----------------------------
        # 4) Passenger timetable engine (later)
        # -----------------------------
        # self.passenger_timetable = PassengerTimetableService(
        #    station_repo=self.repos.stations,
        #    track_section_repo=self.repos.track_sections,
        #    ...
        # )

        # -----------------------------
        # 5) Freight engines (later)
        # -----------------------------

        # IndustryDemandEngine
        # FreightTrainBuilder
        # WaybillGenerator

