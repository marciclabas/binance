from dataclasses import dataclass
from pydantic import BaseModel
from binance.util import ClientMixin
from binance.types import ErrorRoot, BinanceException

class ServerTime(BaseModel):
  serverTime: int
  """Millis timestamp"""

@dataclass
class _ServerTime(ClientMixin):
  @ClientMixin.with_client
  async def server_time(self) -> int:
    """https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#check-server-time"""
    r = await self.client.get(f'{self.base}/api/v3/time')
    obj = r.json()
    if 'code' in obj:
      err = ErrorRoot.model_validate(obj).root
      raise BinanceException(err)
    else:
      return ServerTime.model_validate(obj).serverTime

  