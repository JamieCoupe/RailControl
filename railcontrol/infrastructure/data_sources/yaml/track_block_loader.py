import yaml
import logging

logger = logging.getLogger(__name__)


class TrackBlockYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'track_blocks' exists
        - return raw dict
        """

        logger.debug(f"Loading YAML file: {self.path}")
        track_blocks = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                track_blocks = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(track_blocks, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(track_blocks)}")


        if "track_blocks" not in track_blocks.keys():
            raise KeyError("YAML missing required top-level key 'track_blocks'")

        logger.info(f"Loaded {len(track_blocks)} raw items from {self.path}")
        return track_blocks