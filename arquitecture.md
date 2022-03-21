# Arquitecture

## Rarity calculations
- downloading tokens attributes (requests / openseaAPI)
- calculate rarity based on attributes appearance
- store rarity and rank in my databases
- estimate fair valuations
- for new listings, calculate bargain-ratio and valuation-ratio

## Database 
- Driver: (jsonfiles -> arango -> firestore)
- DB Collections
  - OpenseaCollections
  - Tokens
  - listings? This can absolutely explode... too much info

## API endpoints
- Request a collection to track
- Get rarity rank of a contract & tokenId
- Get valuation ratio (listing price / fair-price)
- Get bargain ratio (fair-price / listing price)

## Infrastructure
- get API keys from Opensea (github repo as page)
- setup nginx configurations for API
- setup my API in new remote server

## Pricing
- donations?
- per month?
- per collection?
- per number of requests?
- a combination of all the above?