import yaml
import logging

logger = logging.getLogger(__name__)


class IndustryYamlLoader:
    def __init__(self, path:str):
        self.path = path

    def load(self):
        """
        - open YAML safely
        - parse
        - ensure top-level 'industries' exists
        - return raw dict
        """
        industry_dict = {}

        with open(self.path, "r") as yaml_file_stream:
            try:
                industry_dict = yaml.safe_load(yaml_file_stream) or {}

            except yaml.YAMLError as e:
                logger.error(f"Error loading yaml {self.path}: {e}")
                raise

        # Validate
        if not isinstance(industry_dict, dict):
            raise ValueError(f"Expected YAML root to be a dict, got {type(industry_dict)}")


        if "industries" not in industry_dict.keys():
            raise KeyError("YAML missing required top-level key 'industries'")

        return industry_dict