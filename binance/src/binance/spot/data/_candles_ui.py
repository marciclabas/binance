from dataclasses import dataclass
from datetime import datetime
from binance.util import ClientMixin, timestamp
from binance.types import ErrorRoot, BinanceException
from ._candles import Candle, CandlesResponse

@dataclass
class _UiCandles(ClientMixin):
  @ClientMixin.with_client
  async def ui_candles(
    self, pair: str, start: datetime | None = None, *,
    interval: str, limit: int = 1000,
  ) -> list[Candle]:
    """https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#uiklines"""
    params  = {'symbol': pair, 'interval': interval, 'limit': limit}
    if start is not None:
      params['startTime'] = timestamp.dump(start)
    r = await self.client.get(f'{self.base}/api/v3/uiKlines', params=params)
    obj = r.json()
    if 'code' in obj:
      err = ErrorRoot.model_validate(obj).root
      raise BinanceException(err)
    else:
      trades = CandlesResponse.model_validate(obj).root
      return list(map(Candle.of, trades))
  