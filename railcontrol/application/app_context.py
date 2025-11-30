import logging

from railcontrol.config import DATA_PATH
from railcontrol.application.routing.routing_service import RoutingService
from railcontrol.application.topology.topology_builder import TopologyBuilder
from railcontrol.infrastructure.providers.repository_provider import RepositoryProvider
from railcontrol.application.timetable.service_id_generator import ServiceIDGenerator

logger = logging.getLogger(__name__)


class AppDataContext:

    def __init__(self, data_path: str = DATA_PATH):
        """
        The application-wide context.
        Builds repositories, services, engines, and exposes them.
        """
        logger.info(f"Starting App Context from: {data_path}")

        # -----------------------------
        # 1) Repository provider
        # -----------------------------
        self.repos = RepositoryProvider(data_path)

        # -----------------------------
        # 2) Build topology builder
        # -----------------------------
        self.topology_builder = TopologyBuilder(
            junction_repository=self.repos.junctions,
            track_section_repository=self.repos.track_sections,
            track_block_repository=self.repos.track_blocks,
            turnout_repository=self.repos.turnouts,
        )

        # -----------------------------
        # 3) Build routing service
        # -----------------------------
        routing_graph = self.topology_builder.build_graph()
        self.routing = RoutingService(routing_graph)

        # -----------------------------
        # 4) Headcode / Service ID Generator  ✓ NEW
        # -----------------------------
        self.service_id_generator = ServiceIDGenerator()

        # Future:
        # self.passenger_timetable = PassengerTimetableService(...)
        # self.freight_engine = IndustryDemandEngine(...)
