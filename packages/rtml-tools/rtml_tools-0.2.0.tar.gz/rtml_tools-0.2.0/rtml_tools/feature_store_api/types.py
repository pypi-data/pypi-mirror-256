from typing import Optional, Union, List, Dict

from pydantic import BaseModel
# import yaml

from rtml_tools.config import YamlConfig

class FeatureGroupConfig(BaseModel):
    """
    Represents a Feature Group in the Hopsworks Feature Store.

    Attributes:
        name (str): Name of the Feature Group
        version (int): Version of the Feature Group
        description (str): Description of the Feature Group
        primary_key (str): Primary key of the Feature Group
        online_enabled (bool): Whether the Feature Group is online enabled
        timestamp (datetime): Timestamp of the trade
    """

    name: str
    version: int
    description: Optional[str] = None
    primary_key: Union[str, List[str]]
    event_time: str
    online_enabled: Optional[bool] = True

    # def to_str(self) -> str:
    #     """
    #     Returns a string representation of the Trade object.
    #     """
    #     return json.dumps(self.model_dump())

    @classmethod
    def from_params(
        cls,
        params: dict
    ) -> "FeatureGroupConfig":
        """
        Returns a FeatureGroupConfig object from a yaml file.
        """
        return cls(**params)
    
class FeatureViewConfig(BaseModel):
    """
    Represents a Feature View in the Hopsworks Feature Store.

    Attributes:
        name (str): Name of the Feature Group
        version (int): Version of the Feature Group
        description (str): Description of the Feature Group
        # from_feature_group (FeatureGroupConfig): The Feature Group to create the Feature View from
    """

    name: str
    version: int
    description: Optional[str] = None
    feature_group_config: Optional[FeatureGroupConfig] = None

    @classmethod
    def from_params(
        cls,
        params: dict,
    ) -> "FeatureViewConfig":
        """
        Returns a FeatureViewConfig object from a yaml file.
        """
        # convert the feature group config to a FeatureGroupConfig object
        feature_group_config = FeatureGroupConfig(**params['feature_group_config'])
        params['feature_group_config'] = feature_group_config
        
        return cls(**params)
    

if __name__ == '__main__':

    from rtml_tools.config import YamlConfig
    yaml_file = '/Users/paulabartabajo/src/real-time-ml-tutorial/config.yml'
    yaml_config = YamlConfig(yaml_file)

    # check we can read a yaml file into a FeatureGroupConfig object
    fg_params = yaml_config.get_feature_group_params('ohlc_feature_group')
    fg_config = FeatureGroupConfig.from_params(fg_params)
    print(fg_config)

    # check we can read a yaml file into a FeatureViewConfig object
    fv_params = yaml_config.get_feature_view_params('ohlc_feature_view')
    fv_config = FeatureViewConfig.from_params(fv_params)
    print(fv_config)