import yaml
import logging

logger = logging.getLogger(__name__)


class StationYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'stations' exists
        - return raw dict
        """
        logger.debug(f"Loading YAML file: {self.path}")
        stations = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                stations = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(stations, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(stations)}")


        if "stations" not in stations.keys():
            raise KeyError("YAML missing required top-level key 'stations'")

        logger.info(f"Loaded {len(stations)} raw items from {self.path}")
        return stations