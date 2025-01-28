# Binance

## Installation

```bash
pip install binance-python
```

## Usage

### Public APIs

You can use specific API clients without authentication. E.g:

```python
from binance.spot import MarketData

client = MarketData()
await client.candles('BTCUSDT', interval='1m', limit=4)
# [Candle(open_time=datetime(...), close_time=datetime(...), open=Decimal('93970.04000000'), ...), ...]
```

### Private API

Easiest is to just use the general client:

```python
from binance import Binance

client = Binance(API_KEY, API_SECRET)
# or client = Binance.env() to load `API_KEY` and `API_SECRET` from environment variables or a .env file

await client.spot_order('BTCUSDT', {
  'price', 10000, ... # let the type hints guide you
})
```

### Context Manager

To run multiple requests concurrently, I'd recommend using the client as a context manager:

```python
from binance import Binance

client = Binance(API_KEY, API_SECRET)

async with client:
  await client.spot_order('BTCUSDT', {
    'price', 10000, ...
  })
  await client.spot_order('ETHUSDT', {
    'price', 2000, ...
  })
```


## Supported APIs

### Spot
- General
  - [ ] Ping
  - [ ] Time
  - [ ] Exchange Information
- Market Data
  - [x] Order Book
  - [x] Recent Trades
  - [x] Old Trades
  - [x] Aggregated Trades
  - [x] Candles
  - [x] UI Candles
  - [x] Average Price
  - [x] Last 24h Price Change Statistics
  - [x] Last Day Price Change Statistics
  - [x] Symbol Price Ticker
  - [ ] ~~Symbol Order Book Ticker~~ Unnecessary: use Order Book instead
  - [x] Window Price Change Statistics
- Trading
  - [ ] New Order
  - [ ] Test New Order
  - [ ] Query Order
  - [ ] Cancel Order
  - [ ] Cancel All Orders
  - [ ] Replace Order
  - [ ] Query Open Orders
  - [ ] Query All Orders
  - [ ] New OCO Order
  - [ ] New OTO Order
  - [ ] New OTOCO Order
  - [ ] Cancel Order List
  - [ ] Query Order List
  - [ ] Query All Order Lists
  - [ ] Query Open Order Lists
  - [ ] New SOR Order
  - [ ] Test SOR Order
- Account
  - [ ] Information
  - [ ] Trade List
  - [ ] Query Unfilled Order Count
  - [ ] Query Prevented Matches
  - [ ] Query Allocations
  - [ ] Query Commission Rates

### Margin
- [ ] Market Data
- [ ] Trading
- [ ] Lending
- [ ] Account
- [ ] Transfer

### Simple Earn
- [ ] Account
- [ ] Earn
- [ ] History

### Wallet
- [ ] Capital
- [ ] Asset
- [ ] Account