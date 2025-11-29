import os
import logging

from src.infrastructure.data_sources.yaml.commodity_loader import CommodityYamlLoader
from src.infrastructure.data_sources.yaml.industry_loader import IndustryYamlLoader
from src.infrastructure.data_sources.yaml.junction_loader import JunctionYamlLoader
from src.infrastructure.data_sources.yaml.track_block_loader import TrackBlockYamlLoader
from src.infrastructure.data_sources.yaml.track_section_loader import TrackSectionYamlLoader
from src.infrastructure.data_sources.yaml.turnout_loader import TurnoutYamlLoader
from src.infrastructure.data_sources.yaml.station_loader import StationYamlLoader

from src.infrastructure.repository.yaml.yaml_commodity_repository import YamlCommodityRepository
from src.infrastructure.repository.yaml.yaml_industry_repository import YamlIndustryRepository
from src.infrastructure.repository.yaml.yaml_junction_repository import YamlJunctionRepository
from src.infrastructure.repository.yaml.yaml_track_block_repository import YamlTrackBlockRepository
from src.infrastructure.repository.yaml.yaml_track_section_repository import YamlTrackSectionRepository
from src.infrastructure.repository.yaml.yaml_turnout_repository import YamlTurnoutRepository
from src.infrastructure.repository.yaml.yaml_station_repository import YamlStationRepository

from src.infrastructure.repository.commodity_repository import CommodityRepository
from src.infrastructure.repository.industry_repository import IndustryRepository
from src.infrastructure.repository.track_block_repository import TrackBlockRepository
from src.infrastructure.repository.track_section_repository import TrackSectionRepository
from src.infrastructure.repository.turnout_repository import TurnoutRepository
from src.infrastructure.repository.station_repository import StationRepository

logger = logging.getLogger(__name__)

class RepositoryProvider:

    # Declare types at class level (recommended)
    commodities: CommodityRepository
    industries: IndustryRepository
    track_blocks: TrackBlockRepository
    track_sections: TrackSectionRepository
    turnouts: TurnoutRepository
    stations: StationRepository

    def __init__(self, base_path: str):
        logger.info(f"Initialising RepositoryProvider using base path: {base_path}")

        industry_loader = IndustryYamlLoader(os.path.join(base_path, "industries.yml"))
        commodity_loader = CommodityYamlLoader(os.path.join(base_path, "commodities.yml"))
        track_block_loader = TrackBlockYamlLoader(os.path.join(base_path, "track_blocks.yml"))
        track_section_loader = TrackSectionYamlLoader(os.path.join(base_path, "track_sections.yml"))
        turnout_loader = TurnoutYamlLoader(os.path.join(base_path, "turnouts.yml"))
        junction_loader = JunctionYamlLoader(os.path.join(base_path, "junctions.yml"))
        station_loader = StationYamlLoader(os.path.join(base_path, "stations.yml"))
        logger.debug("YAML loaders constructed")

        self.commodities = YamlCommodityRepository(commodity_loader)
        logger.info(f"Loaded {len(self.commodities.get_all())} commodities")

        self.industries = YamlIndustryRepository(industry_loader)
        logger.info(f"Loaded {len(self.industries.get_all())} industries")

        self.track_blocks = YamlTrackBlockRepository(track_block_loader)
        logger.info(f"Loaded {len(self.track_blocks.get_all())} track blocks")

        self.track_sections = YamlTrackSectionRepository(track_section_loader)
        logger.info(f"Loaded {len(self.track_sections.get_all())} track sections")

        self.turnouts = YamlTurnoutRepository(turnout_loader)
        logger.info(f"Loaded {len(self.turnouts.get_all())} turnouts")

        self.junctions = YamlJunctionRepository(junction_loader)
        logger.info(f"Loaded {len(self.junctions.get_all())} junctions")

        self.stations = YamlStationRepository(station_loader, self.track_blocks)
        logger.info(f"Loaded {len(self.stations.get_all())} stations")

        if not self.track_sections.get_all():
            raise RuntimeError("No track sections loaded — cannot build topology.")
        logger.info("RepositoryProvider initialisation complete")