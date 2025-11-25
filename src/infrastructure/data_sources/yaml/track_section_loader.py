import yaml
import logging

logger = logging.getLogger(__name__)


class TrackSectionYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'track_sections' exists
        - return raw dict
        """
        track_sections = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                track_sections = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(track_sections, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(track_sections)}")


        if "track_sections" not in track_sections.keys():
            raise KeyError("YAML missing required top-level key 'track_sections'")

        return track_sections