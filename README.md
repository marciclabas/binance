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
  - [x] [Ping](binance/src/binance/spot/general/_ping.py)
  - [x] [Time](binance/src/binance/spot/general/_time.py)
  - [x] [Exchange Information](binance/src/binance/spot/general/_info.py)
- Market Data
  - [x] [Order Book](binance/src/binance/spot/data/_order_book.py)
  - [x] [Recent Trades](binance/src/binance/spot/data/_trades_recent.py)
  - [x] [Old Trades](binance/src/binance/spot/data/_trades_old.py)
  - [x] [Aggregated Trades](binance/src/binance/spot/data/_trades_agg.py)
  - [x] [Candles](binance/src/binance/spot/data/_candles.py)
  - [x] [UI Candles](binance/src/binance/spot/data/_candles_ui.py)
  - [x] [Average Price](binance/src/binance/spot/data/_avg_price.py)
  - [x] [Last 24h Price Change Statistics](binance/src/binance/spot/data/_stats_24h.py)
  - [x] [Last Day Price Change Statistics](binance/src/binance/spot/data/_stats_day.py)
  - [x] [Current Price](binance/src/binance/spot/data/_price.py)
  - [ ] ~~Symbol Order Book Ticker~~ unnecessary: use Order Book instead
  - [x] [Window Price Change Statistics](binance/src/binance/spot/data/_stats.py)
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