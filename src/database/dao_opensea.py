import pandas as pd
from typing import Optional
import requests
import dotenv
from logging import getLogger

dotenv.load_dotenv()


class OpenseaDao:
    def __init__(self):
        self.base_url = "https://api.opensea.io/api/v1"
        self.headers = self._get_headers()
        self.logger = getLogger(self.__class__.__name__)

    def _get_headers(self):
        OPENSEA_API_KEY = os.getenv("OPENSEA_API_KEY")
        assert OPENSEA_API_KEY is not None, "OPENSEA_API_KEY is None"
        return {
            "Accept": "application/json",
            "X-API-KEY": OPENSEA_API_KEY
        }

    def get_all_current_listings(self, collection_slug: str):
        pass

    def _build_query(self, contract_address: str,
                     after_timestamp: Optional[int] = None, cursor: Optional[str] = None,
                     event_type: Optional[str] = None, tokenid: Optional[int] = None,
                     auction_type: Optional[str] = None):
        # url = f"{self.base_url}/events?only_opensea=false"
        url = f"{self.base_url}/events?"
        if tokenid:
            url = f"{url}token_id={tokenid}"
        if contract_address:
            url = f"{url}&asset_contract_address={contract_address}"
        if event_type:
            url = f"{url}&event_type={event_type}"
        if after_timestamp:
            url = f"{url}&occurred_after={after_timestamp}"
        if cursor:
            url = f"{url}&cursor={cursor}"
        if auction_type:
            url = f"{url}&auction_type={auction_type}"

        return url

    def _get_token_events(self, contract_address: Optional[str] = None,
                          event_type: Optional[str] = None,
                          tokenid: Optional[int] = None,
                          after_timestamp: Optional[int] = None,
                          auction_type: Optional[str] = None):
        events = []
        _next = None
        done = False
        while not done:
            try:
                url = self._build_query(
                    contract_address=contract_address,
                    after_timestamp=after_timestamp,
                    tokenid=tokenid,
                    cursor=_next, event_type=event_type,
                    auction_type=auction_type
                )
                # url = "https://api.opensea.io/api/v1/events?token_id=9722&asset_contract_address=0xbce3781ae7ca1a5e050bd9c4c77369867ebc307e&event_type=created"

                response = requests.get(url, headers=self.headers)
                data = response.json()

                # Managing connection and data
                if data.get("detail", "") == 'Request was throttled.':
                    self.logger.exception(data.get("detail", ""))
                    time.sleep(1)
                    continue
                else:
                    if data["next"] is None:
                        done = True
                    else:
                        _next = data["next"]

                self.logger.error(response.status_code)

                # All 'created' events are dutch by default
                for event in data.get("asset_events", []):
                    events.append(event)

                time.sleep(.25)  # API allows up to 4 queries per second only. This assumes one thread

            except Exception as e:
                self.logger.exception("Could not retrieve listings")

        return events


    def get_asset_listing_price(self, contract_address:str, tokenid:int):

        events = self._get_token_events(contract_address, "created", tokenid)




if __name__ == '__main__':
    import requests
    import dotenv
    import os
    import time
    import json
    from os import path

    contract = '0xbce3781ae7ca1a5e050bd9c4c77369867ebc307e'  # goblintownwtf
    # contract = '0x0f78c6eee3c89ff37fd9ef96bd685830993636f2'  # nuclear nerds

    last_timestamp = int(time.time() - 3600 * 24 * 365)

    odao = OpenseaDao()
    tokenids = [9722]

    for tokenid in tokenids:

        events = odao._get_token_events(contract_address=contract, tokenid=9722, event_type='created')

        listings = []
        for event in events:
            # Only events created by the current owner should be considered
            if (event["asset"]["owner"]["address"] == event["seller"]["address"]):
                listings.append(event)
                print(event["event_timestamp"], event["event_type"], event["auction_type"],
                      int(event.get("ending_price", None)) / 1e18,
                      event["asset"]["owner"]["address"], event["seller"]["address"])
