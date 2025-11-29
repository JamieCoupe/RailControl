import yaml
import logging

logger = logging.getLogger(__name__)


class JunctionYamlLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        data = {}
        with open(self.path, "r") as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                logger.error(...)
                raise

        if not isinstance(data, dict):
            raise ValueError("Expected YAML root to be a dict")

        if "junctions" not in data:
            raise KeyError("YAML missing required key 'junctions'")

        return data
