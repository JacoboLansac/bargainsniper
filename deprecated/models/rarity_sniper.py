import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path
from deprecated.opensea_objects.opensea_asset import OpenseaAsset
from deprecated.opensea_objects.opensea_collection import OpenseaCollection
import plotly.express as px
import plotly.graph_objects as go
import jacotools as jtools
from jacotools import notificators
import nftconfigs as cfg
from scipy.optimize import curve_fit

LINK = 'link'
TOKEN_ID = 'token_id'
ETHPRICE = 'eth_price'
RARITY = 'rarity'
OUTLTHRESHOLD = 'OutliersThreshold'
BARGTHRESHOLD = 'BargainThreshold'
RANK = 'rarity_rank'
BARGINDEX = 'bargain_index'
OPPORTUNITY = 'Opportunity'


class RaritySniper:
    def __init__(self, slug: str, max_eth_price: float = None, outliers_perc=.05, bargain_thresh_perc=.5):
        self.slug = slug
        self.outliers_perc = outliers_perc
        self.bargain_thresh_perc = bargain_thresh_perc
        self.collection = OpenseaCollection(self.slug)
        self.telegramer = notificators.Telegramer(self.__class__.__name__, cooldown_freq='2d')

        self.title = f"{slug}. Total suply={self.collection.total_supply} items"
        self.max_eth_price = max_eth_price
        self.collectionpath = path.join(cfg.datapath, 'tmp' if jacotools.is_debugging() else 'figures', self.slug)
        os.makedirs(self.collectionpath, exist_ok=True)

    def load_asset_data(self, nassets: int, per_page=50):
        t = time.time()
        print(f"Retrieving {nassets} from {self.slug}")
        assetslist = []
        for offset in range(0, nassets, per_page):
            assets_data = self.collection.query_collection_items(offset, per_page)
            if not assets_data:
                break
            for asset_dict in assets_data:
                asset = OpenseaAsset(asset_dict, self.collection)
                if (asset.eth_price is not None) and (asset.eth_price < self.collection.floor_price):
                    print(f"price lower than floor price. Order: {asset.orders}")

                assetslist.append({
                    TOKEN_ID: asset.token_id,
                    ETHPRICE: asset.eth_price,
                    RARITY: asset.rarity,
                    LINK: asset.link,
                })
        data = pd.DataFrame(assetslist).head(nassets)
        print(f"[{self.collection.slug}]: Loaded {len(assetslist)} assets. "
              f"{jtools.get_time_in_nice_format(time.time() - t)} seconds")
        return data

    def mark_outliers(self, data: pd.DataFrame, window=100, quant=.01) -> pd.DataFrame:

        def curve(x, a, b):
            return a / x + b

        if len(data) < 3:
            print(f"Not enough data to fit")
            data[OUTLTHRESHOLD] = 0
            data[BARGTHRESHOLD] = 0
        else:
            data.set_index('rarity_rank', inplace=True)
            low_points = data[ETHPRICE].dropna().rolling(window, min_periods=1).quantile(quant)

            X = low_points.index.values + 1
            Y = low_points.values
            params, _ = curve_fit(curve, X, Y, (0, 0))
            xoffset = 50
            fair_floor = curve(data.index.values + xoffset, *params)
            data[OUTLTHRESHOLD] = (1 - self.outliers_perc) * fair_floor
            data[BARGTHRESHOLD] = (1 - self.bargain_thresh_perc) * fair_floor

        data[OPPORTUNITY] = (data[BARGTHRESHOLD] > data[ETHPRICE])
        data.reset_index(inplace=True)
        return data

    def plot_interactive_scatter(self, data: pd.DataFrame):
        fig1 = px.scatter(data, x=RANK, y=ETHPRICE, hover_data=[TOKEN_ID, BARGINDEX], size=BARGINDEX, title=self.title)
        fig2 = px.line(data, x=RANK, y=OUTLTHRESHOLD, title=OUTLTHRESHOLD)  # This line is the threshold
        fig3 = px.line(data, x=RANK, y=BARGTHRESHOLD, title=BARGTHRESHOLD)  # This line is the threshold
        fig = go.Figure(data=fig1.data + fig2.data + fig3.data)
        if not data[RANK].empty:
            fig.update_layout(yaxis_range=[0, 2 * self.max_eth_price], xaxis_range=[0, max(data[RANK])])
        filepath = path.join(self.collectionpath, 'scatter_{}_vs_{}.html'.format(RANK, ETHPRICE))
        fig.write_html(filepath)
        return filepath

    def save_csv(self, df: pd.DataFrame):
        csvfpath = path.join(self.collectionpath, f'csv_{RARITY}_vs_{ETHPRICE}.csv')
        df[df[ETHPRICE] < self.max_eth_price].sort_values(by=BARGINDEX, ascending=False).to_csv(csvfpath, index=False)

    def run(self, max_n_assets=None):
        # Retrieve all assets from Open sea
        nassets = max_n_assets or self.collection.total_supply
        data = self.load_asset_data(nassets)
        # Data analysis
        print(f"{self.slug}: {len(data)} assets")
        df = pd.DataFrame(data)
        # The rank based on rarity is given before dropping Nans, to include also those without price
        df = df.sort_values(by=RARITY, ascending=False).reset_index(drop=True)
        df.dropna(inplace=True)
        df[BARGINDEX] = df[RARITY].divide(df[ETHPRICE])
        df = df[~(df == np.inf).any(axis=1)].copy()
        df[RANK] = df.index.values
        df[BARGINDEX] = df[BARGINDEX].round(2)
        df = self.mark_outliers(df)
        print(f"{self.slug}: {len(df)} with price")

        # Save to csv
        self.save_csv(df)

        # Plot price distribution
        distribution_fname = path.join(self.collectionpath, 'distribution_{}.png')
        for metric in [ETHPRICE, RARITY, BARGINDEX]:
            plt.close("all")
            df[df[ETHPRICE] < df[ETHPRICE].quantile(.5)][metric].hist(bins=100, alpha=.75)
            plt.ylabel('count')
            plt.xlabel(metric)
            plt.title(self.title)
            plt.tight_layout()
            plt.savefig(distribution_fname.format(metric), dpi=120)

        # Plotting scatter pairs
        pairs = [
            (RANK, ETHPRICE),
            # (RANK, RARITY),
        ]
        # Filter those above specific price. ONLY AFTER SAVING THE DISTRIBUTIONS
        df = df[df[ETHPRICE].between(0, self.max_eth_price)].copy()
        df = df[df[RANK] < df[RANK].quantile(.5)].copy()
        if df.empty:
            print(f"Empty data after filtering")
            return 

        self.plot_interactive_scatter(df)

        scatter_templ = path.join(self.collectionpath, 'scatter_{}_vs_{}{}.png')
        for metx, mety in pairs:
            ymax = df[ETHPRICE].quantile(.9) if not df[ETHPRICE].empty else None
            plt.close("all")
            plt.scatter(df[metx], df[mety], s=5, alpha=.25)
            textdf = df[(df[OUTLTHRESHOLD] > df[ETHPRICE]) & (df[ETHPRICE] < ymax)]
            plt.scatter(textdf[metx], textdf[mety], s=5, alpha=.25, c='r')
            [plt.text(r[metx], r[mety], r[TOKEN_ID], alpha=.35, rotation=45, horizontalalignment='right',
                      verticalalignment='top') for _, r in textdf.iterrows()]
            plt.plot(df[RANK], df[OUTLTHRESHOLD], c='r', alpha=.5)
            plt.plot(df[RANK], df[BARGTHRESHOLD], c='gold', alpha=.5)
            plt.xlabel(f"{metx}")
            plt.ylabel(f"{mety}")
            ylim = plt.ylim()
            plt.ylim(max(ylim[0], 0), ymax)
            plt.title(self.title)
            plt.tight_layout()
            plt.savefig(scatter_templ.format(metx, mety, ''), dpi=120)
            # [plt.text(r[metx], r[mety], r[TOKEN_ID], alpha=.35, rotation=45, horizontalalignment='right',
            #           verticalalignment='top') for _, r in df.iterrows()]
            # plt.savefig(scatter_templ.format(metx, mety, '_text'), dpi=120)

        oppp = df[df[OPPORTUNITY]].copy()
        if not oppp.empty:
            message = "\n".join([f"{self.slug} #{r[TOKEN_ID]}: RANK: {r[RANK]}" for _,r in oppp.iterrows()])
            figurepaths = [distribution_fname.format(ETHPRICE), scatter_templ.format(RANK, ETHPRICE, '')]
            self.telegramer.notify(self.slug, message, figurepaths=figurepaths)


if __name__ == '__main__':
    rs = RaritySniper('cryptozombieznft', max_eth_price=3, )
    rs.run(max_n_assets=None)
