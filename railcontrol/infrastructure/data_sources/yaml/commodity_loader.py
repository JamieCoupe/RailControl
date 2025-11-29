import yaml
import logging

logger = logging.getLogger(__name__)


class CommodityYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'commodities' exists
        - return raw dict
        """
        logger.debug(f"Loading YAML file: {self.path}")
        commodities = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                commodities = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(commodities, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(commodities)}")


        if "commodities" not in commodities.keys():
            raise KeyError("YAML missing required top-level key 'commodities'")

        logger.info(f"Loaded {len(commodities)} raw items from {self.path}")
        return commodities