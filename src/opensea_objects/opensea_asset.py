import numpy as np
import pandas as pd


class OpenseaAsset:
    def __init__(self, data: dict, collection):
        self.collection = collection  # OpenseaCollection object
        self.link = data['permalink']
        self.traits = data['traits']
        self.token_id = data['token_id']
        self.asset_contract = data['asset_contract']['address']
        self.orders = data.get('sell_orders') or []
        self.eth_price = self.get_ether_price()
        self.rarity = self._estimate_rarity()
        self.owner_address = data['owner']['address']
        # self.owner_name = data['owner']['user']['username']

    def get_ether_price(self):
        """
        Filters buy orders and determines the price in ETH
        :return:
        """
        decimals = 18  # This should be done better

        sell_orders = []
        for order in self.orders:
            if order['side'] != 1:  # side=1 is sell order, side=0 is a buy order
                continue
            if order['sale_kind'] != 0:  # This filters dutch auctions
                continue
            if (order['static_extradata'] != '0x'):  # This filters out prices below floor price (I think)
                continue
            if order['cancelled'] or order['finalized'] or order['marked_invalid']:
                continue
            if pd.Timestamp(order['expiration_time'], unit='s') < pd.Timestamp.now():
                continue
            if pd.Timestamp(order['closing_date']) < pd.Timestamp.now():
                continue

            # fields = 'sale_kind how_to_call side fee_method maker taker static_target static_extradata'.split()
            # print({f:order[f] for f in fields})
            sell_orders.append(order)

        potential_prices = [float(order['current_price']) / 10 ** decimals for order in sell_orders]
        final_price = min(potential_prices) if potential_prices else None

        # Specific for YawkuzaCats
        # suspicious_price_thresh = .2
        # if (final_price is not None) and (final_price < suspicious_price_thresh):
        #     print(f"item [{self.token_id}]: price below {suspicious_price_thresh}")
    
        return final_price

    # def _get_decimals(self, pay_with_token: ETH):
    #     payment_tokens = self.collection['payment_tokens']
    #     for payment_token in payment_tokens:
    #         if payment_token['symbol'] == pay_with_token:
    #             decimals = payment_token['decimals']
    #             return decimals

    def _estimate_rarity(self):
        if not self.traits:
            return None
        else:
            traits = self.traits
            traitsdf = pd.DataFrame(traits)
            traitsdf['trait_probability'] = traitsdf['trait_count'] / self.collection.total_supply
            traitsdf = traitsdf[traitsdf['trait_probability'] > 0].copy()
            # Some traits have probability zero for some weird reason
            return np.log(1000 / traitsdf['trait_probability'].cumprod().iloc[-1])

