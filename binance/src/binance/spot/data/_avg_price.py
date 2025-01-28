from dataclasses import dataclass
from pydantic import BaseModel
from binance.util import ClientMixin, timestamp
from binance.types import ErrorRoot, BinanceException

class AvgPrice(BaseModel):
  mins: int
  """Avg. price interval"""
  price: str
  closeTime: int
  """Last trade time (millis timestamp)"""

@dataclass
class _AvgPrice(ClientMixin):
  @ClientMixin.with_client
  async def avg_price(
    self, pair: str,
  ) -> AvgPrice:
    """https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#current-average-price"""
    params  = {'symbol': pair }
    r = await self.client.get(f'{self.base}/api/v3/avgPrice', params=params)
    obj = r.json()
    if 'code' in obj:
      err = ErrorRoot.model_validate(obj).root
      raise BinanceException(err)
    else:
      return AvgPrice.model_validate(obj)
  