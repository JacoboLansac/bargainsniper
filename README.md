# Bargain sniper

## Description

An API service to detect under-priced NFTs from Opensea market place. The under-price criteria is decided by compared the listing
price with an estimated fair price in eth which compares each listing with the entire collection.

## Motivation

Many times, an asset is listed at an underprcied valuation but we miss it just because the price is slightly above floor price
This API aims to give users the chance of sniping these underpriced items by looking at some more complex
metrics relating price and rarity ranking. 

## API endpoints

The API offers the following end-points:

#### Rarity rank

Gets the rarity rank of a collection

      GET: /api/token/rarity-rank/<collection_id>/

#### Estimated fair price

Gets the estimated fair price in eth of a token

      GET: /api/token/fair-eth-price/<collection_id>/<tokenid>/

#### Bargain factor

Get the esitmated bargain factor of a tokenid (fair price to listing price)

      GET: /api/token/bargain-factor/<collection_id>/<tokenid>/

#### Collection availability

Asks if a collection is currently available, meaning that it is being tracked currently by our databases

      GET: /api/collection/is-available/<collection_id>/

#### Request new collection

Requests a new colleciton to be tracked by the bot. Requires an authentication token. For now this functinoality
isdisabled until authentication system is setup.

      POST: /api/collection/request/<collection_id>/

### Authenticatoin

To be defined.

## Installation

    pip install -r requirements.txt

## References & Documentation

### Opensea API

https://docs.opensea.io/reference/retrieving-a-single-asset
