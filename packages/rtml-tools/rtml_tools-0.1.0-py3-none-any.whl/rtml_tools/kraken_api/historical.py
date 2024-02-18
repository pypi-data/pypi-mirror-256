from typing import List, Optional, Union
from datetime import datetime, timezone, timedelta
import logging
from pathlib import Path
import json
import os
from time import sleep

import requests

from rtml.kraken_api.types import Trade

logger = logging.getLogger()


MAP_PRODUCT_IDS = {
    "XBT/EUR": "XXBTZEUR",
}

class KrakenHistoricalTradesAPI:

    BASE_URL = "https://api.kraken.com"

    def __init__(
        self,
        product_id: Optional[str] = "XBT/EUR",
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        log_enabled: bool = True,
        cache_dir: Optional[str] = None,
    ):  
        self.product_id = product_id

        # map product_id from the usual format (e.g. "XBT/EUR")
        # to the format required by Kraken API (e.g. "XXBTZEUR")
        self.kraken_api_product_id = self._map_product_id_to_kraken_api_format(product_id)

        # set default values of last 30 days if no from_date and to_date are provided
        utc_now = datetime.now(timezone.utc)
        self.from_date = from_date if from_date else utc_now - timedelta(days=30)
        self.to_date = to_date if to_date else utc_now
        
        # convert datetime to nanoseconds, which is the format required by Kraken API
        self._from_date_ns = int(self.from_date.timestamp() * 1e9)
        self._to_date_ns = int(self.to_date.timestamp() * 1e9)
        
        # last fetched timestamp, so we know if we need to fetch more trades
        self._last_fetched_timestamp_ns = self._from_date_ns

        # last batch of trades fetched from Kraken API
        # self._trades = None

        self._log_enabled = log_enabled

        # caching of trade data into local files
        self._use_cache = False
        if cache_dir is not None:
            # Create the directory if it doesn't exist
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            self._cache_dir = cache_dir
            self._use_cache = True


    def get_trades(self) -> Union[List[Trade], None]:
        
        # check if we have already fetched all trades
        if self._last_fetched_timestamp_ns > self._to_date_ns:
            self._log('No more trades to fetch from Kraken API')
            return None

        # fetch a batch of trades from Kraken API
        trades : List[List] = self._download_batch_of_trades_from_kraken()

        # convert trades : List[List] -> List[Trade]
        trades : List[Trade] = [self.parse_trade_obj(trade) for trade in trades]

        # make sure trades are sorted by timestamp
        trades = sorted(trades, key=lambda x: x.timestamp)

        # keep last timestamp in the batch in nanoseconds
        self._last_fetched_timestamp_ns = trades[-1].timestamp * 1e6

        return trades
        
    def parse_trade_obj(self, trade: List) -> Trade:
        """Parses the trade object returned by Kraken API into a Trade object."""
        # breakpoint()
        return Trade(
            product_id=self.product_id,
            price=float(trade[0]),
            volume=float(trade[1]),
            timestamp=int(float(trade[2]) * 1000), # milliseconds
        )
    
    def _download_batch_of_trades_from_kraken(self) -> List[List]:
        """
        Downloads a batch of trades from Kraken API.

        Returns:
            List[Trade]: A list of Trade objects.
        """
        # fetch a batch of trades from Kraken API
        url = f"{self.BASE_URL}/0/public/Trades?pair={self.kraken_api_product_id}&since={self._last_fetched_timestamp_ns:.0f}"
        
        if self._use_cache:
            # check if we have already fetched these trades
            file_name = generate_filename_from_hash(url)
            trades = self._load_trades_file_from_cache(file_name)
            if trades is not None:
                self._log(f'Loaded trades from cache file {file_name}')
                return trades

        response = requests.get(url)
        
        # sleep for 1 second to avoid hitting the rate limit of Kraken API
        sleep(1)
        
        if response.status_code == 200:
            try:
                trades = response.json()["result"][self.kraken_api_product_id]
                self._log(f'Trades successfully fetched from Kraken API. ')
            except KeyError as e:
                logger.error('Response 200 but no data in it...')
                logger.error(f'Response={response}')
                pass
        else:
            logger.error(f"Failed to fetch trades from Kraken API. Response={response}")
            raise Exception(f"400 status code. Response={response}")
        
        if self._use_cache:
            file_name = generate_filename_from_hash(url)
            self._save_trades_file_to_cache(file_name, trades=trades)

        return trades

    def _load_trades_file_from_cache(self, file_name: str) -> Union[List[list], None]:
        
        file_path = Path(self._cache_dir) / file_name
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as file:
                # trades = file.read()
                trades = json.load(file)
        
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Failed to load trades from cache file {file_path}")
            # remove file_path
            os.remove(file_path)
            return None
        
        return trades
    
    def _save_trades_file_to_cache(self, file_name: str, trades: List[list]) -> None:
        
        file_path = Path(self._cache_dir) / file_name
        with open(file_path, 'w') as file:
            # breakpoint()
            # file.write(trades)
            json.dump(trades, file)

    def _map_product_id_to_kraken_api_format(self, product_id: str) -> str:
        """
        Maps a product_id from the usual format (e.g. "XBT/EUR")
        to the format required by Kraken API (e.g. "XXBTZEUR").
        """
        try:
            return MAP_PRODUCT_IDS[product_id]
        except KeyError:
            logger.error(f"Invalid product_id={product_id}. Valid product_ids are {list(MAP_PRODUCT_IDS.keys())}")
            raise ValueError(f"Invalid product_id={product_id}. Valid product_ids are {list(MAP_PRODUCT_IDS.keys())}")

    def _log(self, msg: str) -> None:
        if self._log_enabled:
            logger.info(f'[KrakenHistoricalTradesAPI] {msg}')
            
def generate_filename_from_hash(long_string, hash_length=8):

    import hashlib

    # Calculate the hash of the long string
    hash_value = hashlib.sha256(long_string.encode()).hexdigest()
    # Take the first `hash_length` characters of the hash
    filename = hash_value[:hash_length]
    return filename

if __name__ == '__main__':

    kraken_historical_api = KrakenHistoricalTradesAPI(
        product_id="XBT/EUR",
        from_date=datetime(2021, 1, 1),
        to_date=datetime(2021, 1, 2),
        cache_dir='../.cache/trades',
        log_enabled=True,
    )

    trades = kraken_historical_api.get_trades()
    while trades is not None:
        print(f'Fetched trades from {trades[0].timestamp} to {trades[-1].timestamp}')
        trades = kraken_historical_api.get_trades()