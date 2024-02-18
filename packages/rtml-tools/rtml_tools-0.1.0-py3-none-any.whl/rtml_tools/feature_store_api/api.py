import os
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timedelta

import hopsworks
import hsfs
import pandas as pd

from rtml.feature_store_api.types import FeatureGroupConfig, FeatureViewConfig

logger = logging.getLogger()

class FeatureGroup:
    """A wrapper around the Hopsworks Feature Group class."""
    def __init__(
        self,
        feature_group: hsfs.feature_group.FeatureGroup,
    ):  
        self._fg = feature_group
        self.name = self._fg.name
        self.version = self._fg.version
        
    def write(
        self,
        value: Dict[str, Any],
        keys: Optional[list] = None,
        online_only: Optional[bool] = True,
    ) -> None:
        # If `keys` is prvovided, only keep these in the value
        _value = {k: value[k] for k in keys} if keys else value
        logger.info(f'Writing {_value} to feature group {self._fg.get_fg_name()}')

        # Convert the value to a Pandas DataFrame
        df = pd.DataFrame.from_records([_value])

        # Write the DataFrame to the feature group
        # logger.info(f'Writing {df} to feature group {self._fg}')
        if online_only:
            job, _ = self._fg.insert(
                df,
                write_options={
                    "start_offline_backfill": False,
                    "wait_for_job": False,
                }
            )
        else:
            raise NotImplementedError("Offline writing not implemented yet")

        # return job
        
class FeatureView:
    """
    A wrapper around the Hopsworks Feature View class.
    It only supports defining a FeatureView that selects all columns from a single FeatureGroup.
    """
    def __init__(
        self,
        feature_view: hsfs.feature_view.FeatureView,
    ):
        self._fv = feature_view

    def read(
        self,
        primary_keys: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """Reads features from the online feature store."""
        return self._fv.get_feature_vectors(
            entry=primary_keys,
            return_type="pandas"
        )
        # return self._fv.get_feature_vectors(entry=primary_keys,return_type="pandas")

    def read_offline(
        self,
        from_date: datetime,
        to_date: datetime,
    ) -> pd.DataFrame:
        """Reads features from the offline feature store."""

        # get data from 28 days before and after from_date and to_date
        # we add this margin to make sure we have all the data we need
        data = self._fv.get_batch_data(
            start_time=from_date - timedelta(days=28),
            end_time=to_date + timedelta(days=28)
        )
        # TODO: might need to add exception handling here
        # if no training data was generated from this feature view
        # before calling .get_batch_data()
        # data, _ = self._fv.training_data()

        # keep only data between from_date and to_date
        from_ms = int(from_date.timestamp() * 1000)
        to_ms = int(to_date.timestamp() * 1000)
        data = data[data.timestamp.between(from_ms, to_ms)]
        
        # sort data by timestamp
        data = data.sort_values(by=['timestamp'])

        return data
    
class FeatureStore:
    """A wrapper around the Hopsworks Feature Store class."""
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        self._api_key = api_key
        if self._api_key is None:
            try:
                self._api_key = os.environ["HOPSWORKS_API_KEY"]
            except KeyError:
                raise KeyError(
                    "No HOPSWORKS_API_KEY provided. Please provide an API key or set the HOPSWORKS_API_KEY environment variable."
                )

        self._project_name = project_name
        if self._project_name is None:
            try:
                self._project_name = os.environ["HOPSWORKS_PROJECT_NAME"]
            except KeyError:
                raise KeyError(
                    "No HOPSWORKS_PROJECT_NAME provided. Please provide a project name or set the HOPSWORKS_PROJECT_NAME environment variable."
                )
        
        # First connect to the jobs api
        self._jobs_api = self._get_jobs_api()
        # then to the Feature Store
        self._fs = self._get_feature_store()
        # otherwise, I get 
        # Exception("Couldn't find client. Try reconnecting to Hopsworks.")

    def get_feature_group(self, feature_group_config: FeatureGroupConfig) -> FeatureGroup:
        """
        Returns an existing feature group.
        """
        fg = self._fs.get_feature_group(
            name=feature_group_config.name,
            version=feature_group_config.version,
        )

        return FeatureGroup(fg)
    
    def get_or_create_feature_group(self, feature_group_config: FeatureGroupConfig) -> FeatureGroup:
        """
        Creates a feature group in the feature store if it does not exist, otherwise returns the existing feature group.
        """
        logger.info(f"Creating feature group {feature_group_config}")
        
        fg = self._fs.get_or_create_feature_group(
            name=feature_group_config.name,
            version=feature_group_config.version,
            description=feature_group_config.description,
            primary_key=feature_group_config.primary_key,
            event_time=feature_group_config.event_time,
            online_enabled=feature_group_config.online_enabled
        )

        logger.info(f"Created feature group {fg}")

        return FeatureGroup(fg)
    
    def get_or_create_feature_view(self, feature_view_config: FeatureViewConfig) -> FeatureView:
        
        # it only supports defining a feature view that selects all columns from a
        # single feature group
        fg = self.get_feature_group(feature_view_config.feature_group_config)
        query = fg._fg.select_all()

        fv = self._fs.get_or_create_feature_view(
            name=feature_view_config.name,
            version=feature_view_config.version,
            description=feature_view_config.description,
            query=query
        )
        return FeatureView(fv)

    def materialize(self, feature_group: FeatureGroup) -> None:    
        """
        Materializes the online feature group to the offline feature group.
        """
        job_name = f'{feature_group.name}_{feature_group.version}_offline_fg_materialization'
        backfill_job = self._jobs_api.get_job(job_name)
        execution = backfill_job.run(await_termination=True)
        logger.info(f'Backfill job {job_name} finished with status {execution.success}')

    def _get_jobs_api(self) -> "JobsAPI":
        
        project = hopsworks.login(
            project=self._project_name,
            api_key_value=self._api_key,
        )
        return project.get_jobs_api()
    
    def _get_feature_store(self) -> hsfs.feature_store.FeatureStore:
        project = hopsworks.login(
            project=self._project_name,
            api_key_value=self._api_key,
        )
        return project.get_feature_store()

if __name__ == '__main__':

    from rtml.config import YamlConfig
    yaml_file = '/Users/paulabartabajo/src/real-time-ml-tutorial/config.yml'
    yaml_config = YamlConfig(yaml_file)

    # get feature view config from yaml file
    fv_params = yaml_config.get_feature_view_params('ohlc_feature_view')
    fv_config = FeatureViewConfig.from_params(fv_params)

    # get or create feature view
    fs = FeatureStore(
        api_key=os.environ["HOPSWORKS_API_KEY"],
        project_name=os.environ["HOPSWORKS_PROJECT_NAME"],
    )
    fv = fs.get_or_create_feature_view(fv_config)

    # get batch of features between given dates
    data = fv.read_offline(
        from_date=datetime(2024, 1, 1),
        to_date=datetime(2024, 1, 30),
    )
    print(data)

