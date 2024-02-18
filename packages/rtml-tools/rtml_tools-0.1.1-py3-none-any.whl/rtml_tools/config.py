from typing import Union
from pathlib import Path

import yaml

class YamlConfig:

    """Interface to the YAML configuration file."""

    def __init__(self, yaml_file: Union[str, Path]):
        
        self._yaml_file = yaml_file
        self._config = self._load_config_from_yaml(yaml_file)

    def _load_config_from_yaml(self, yaml_file: Union[str, Path]) -> dict:
        """Loads a YAML file and returns a dictionary."""
        with open(yaml_file, "r") as f:
            yaml_dict = yaml.safe_load(f)
        return yaml_dict
    
    def get_feature_group_params(self, name: str) -> dict:
        return self._config['feature_groups'][name]
    
    def get_feature_view_params(self, name: str) -> dict:
        config = self._config['feature_views'][name]
        config['feature_group_config'] = self.get_feature_group_params(config['feature_group'])
        return config
    
    def get_param(self, name: str) -> dict:
        return self._config[name]
    
    # @classmethod
    # def from_yaml(cls, yaml_file: Union[str, Path]) -> "GlobalConfig":
    #     """Returns a GlobalConfig object from a yaml file."""
    #     return cls(yaml_file)