from dataclasses import dataclass
from binance.util import ClientMixin
from binance.types import ErrorRoot, BinanceException

@dataclass
class _Ping(ClientMixin):
  @ClientMixin.with_client
  async def ping(self):
    """https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#test-connectivity"""
    r = await self.client.get(f'{self.base}/api/v3/ping')
    obj = r.json()
    if 'code' in obj:
      err = ErrorRoot.model_validate(obj).root
      raise BinanceException(err)

  