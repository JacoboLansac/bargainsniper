# Bargain sniper

## Description

A bot to detect
under-priced NFTs from Opensea market place. The under-price criteria is decided by compared the
listing price with an estimated fair price in eth which compares each listing with the entire collection.

### API endpoints

The end product is an API that offers the following end-points:

- Get the rarity rank of a collection

      GET: /api/token/rarity-rank/<collection_id>/

- Get the estimated fair price in eth of a token

      GET: /api/token/fair-eth-price/<collection_id>/<tokenid>/

- Get the esitmated bargain factor of a tokenid (fair price to listing price)

      GET: /api/token/bargain-factor/<collection_id>/<tokenid>/

- Asks if a collection is currently being tracked by our databases

      GET: /api/collection/is-available/<collection_id>/

- Requests a new colleciton to be tracked by the bot

      POST: /api/collection/request/<collection_id>/

## Installation

    pip install -r requirements.txt

## References & Documentation

### Opensea API

https://docs.opensea.io/reference/retrieving-a-single-asset
