import yaml
import logging

logger = logging.getLogger(__name__)


class TurnoutYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'turnout' exists
        - return raw dict
        """
        logger.debug(f"Loading YAML file: {self.path}")
        turnouts = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                turnouts = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(turnouts, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(turnouts)}")


        if "turnouts" not in turnouts.keys():
            raise KeyError("YAML missing required top-level key 'turnouts'")

        logger.info(f"Loaded {len(turnouts)} raw items from {self.path}")
        return turnouts