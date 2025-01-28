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

await client.spot.new_order('BTCUSDT', {
  'price', 10000, ... # let the type hints guide you
})
```

### Context Manager

To run multiple requests concurrently, I'd recommend using the client as a context manager:

```python
from binance import Binance

client = Binance(API_KEY, API_SECRET)

async with client:
  await client.spot.new_order('BTCUSDT', {
    'price', 10000, ...
  })
  await client.spot.new_order('ETHUSDT', {
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
  - [x] [New Order](binance/src/binance/spot/trading/_new_order.py)
  - [x] [Test New Order](binance/src/binance/spot/trading/_test_order.py)
  - [x] [Query Order](binance/src/binance/spot/trading/_query_order.py)
  - [x] [Cancel Order](binance/src/binance/spot/trading/_cancel_order.py)
  - [x] [Cancel Open Orders](binance/src/binance/spot/trading/_cancel_open_orders.py)
  - [x] [Replace Order](binance/src/binance/spot/trading/_replace_order.py)
  - [x] [Query Open Orders](binance/src/binance/spot/trading/_query_open_orders.py)
  - [x] [Query All Orders](binance/src/binance/spot/trading/_query_all_orders.py.py)
  - [x] [New OCO Order](binance/src/binance/spot/trading/_oco_order.py)
  - [x] [New OTO Order](binance/src/binance/spot/trading/_oto_order.py)
  - [x] [New OTOCO Order](binance/src/binance/spot/trading/_otoco_order.py)
  - [x] [Cancel Order List](binance/src/binance/spot/trading/_cancel_order_list.py)
  - [ ] ~~Query Order List~~: support unplanned
  - [ ] Query ~~All Order Lists~~: support unplanned
  - [ ] Query ~~Open Order Lists~~: support unplanned
  - [ ] ~~New SOR Order~~: support unplanned
  - [ ] ~~Test SOR Order~~: support unplanned
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