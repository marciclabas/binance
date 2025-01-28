from dataclasses import dataclass
from pydantic import RootModel
from binance.util import ClientMixin
from binance.types import ErrorRoot, BinanceException
from ._trades_recent import Trade, TradeResponse

@dataclass
class _OldTrades(ClientMixin):
  @ClientMixin.with_client
  async def old_trades(self, symbol: str, *, limit: int = 500, fromId: int | None = None) -> list[Trade]:
    """https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints#old-trade-lookup"""
    params = { 'symbol': symbol, 'limit': limit }
    if fromId is not None:
      params['fromId'] = fromId
    r = await self.client.get(f'{self.base}/api/v3/historicalTrades', params=params)
    obj = r.json()
    if 'code' in obj:
      err = ErrorRoot.model_validate(obj).root
      raise BinanceException(err)
    else:
      return TradeResponse.model_validate(obj).root