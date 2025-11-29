import yaml
import logging

logger = logging.getLogger(__name__)


class PassengerRouteYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'passenger_routes' exists
        - return raw dict
        """
        logger.debug(f"Loading YAML file: {self.path}")
        passenger_routes = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                passenger_routes = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(passenger_routes, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(passenger_routes)}")


        if "passenger_routes" not in passenger_routes.keys():
            raise KeyError("YAML missing required top-level key 'passenger_routes'")

        logger.info(f"Loaded {len(passenger_routes.get("passenger_routes", []))} raw items from {self.path}")
        return passenger_routes