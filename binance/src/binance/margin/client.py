from typing_extensions import Literal, overload
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from binance.util import UserMixin, binance_timestamp, validate_response
from binance.types import Error

class BorrowResponse(BaseModel):
  tranId: int
  code: Literal[None] = None

@dataclass
class _Borrow(UserMixin):
  @overload
  async def borrow(self, *, asset: str, amount: str, recvWindow: int = 5000, isolated: Literal[False] = False, unsafe: Literal[False] = False) -> BorrowResponse | Error:
    ...
  @overload
  async def borrow(self, *, asset: str, amount: str, recvWindow: int = 5000, isolated: Literal[False] = False, unsafe: Literal[True]) -> BorrowResponse:
    ...
  @overload
  async def borrow(self, *, asset: str, symbol: str, recvWindow: int = 5000, amount: str, isolated: Literal[True], unsafe: Literal[False] = False) -> BorrowResponse | Error:
    ...
  @overload
  async def borrow(self, *, asset: str, symbol: str, recvWindow: int = 5000, amount: str, isolated: Literal[True], unsafe: Literal[True]) -> BorrowResponse:
    ...
  async def borrow(self, *, asset: str, symbol: str | None = None, recvWindow: int = 5000, amount: str, isolated: bool = False, unsafe: bool = False):
    return await self._borrow_repay('BORROW', asset=asset, symbol=symbol, recvWindow=recvWindow, amount=amount, isolated=isolated, unsafe=unsafe)
  
  @overload
  async def repay(self, *, asset: str, amount: str, recvWindow: int = 5000, isolated: Literal[False] = False, unsafe: Literal[False] = False) -> BorrowResponse | Error:
    ...
  @overload 
  async def repay(self, *, asset: str, amount: str, recvWindow: int = 5000, isolated: Literal[False] = False, unsafe: Literal[True]) -> BorrowResponse:
    ...
  @overload
  async def repay(self, *, asset: str, symbol: str, recvWindow: int = 5000, amount: str, isolated: Literal[True], unsafe: Literal[False] = False) -> BorrowResponse | Error:
    ...
  @overload
  async def repay(self, *, asset: str, symbol: str, recvWindow: int = 5000, amount: str, isolated: Literal[True], unsafe: Literal[True]) -> BorrowResponse:
    ...
  async def repay(self, *, asset: str, symbol: str | None = None, recvWindow: int = 5000, amount: str, isolated: bool = False, unsafe: bool = False):
    return await self._borrow_repay('REPAY', asset=asset, symbol=symbol, recvWindow=recvWindow, amount=amount, isolated=isolated, unsafe=unsafe)

  async def _borrow_repay(self, type: Literal['BORROW', 'REPAY'], *, asset: str, symbol: str | None = None, recvWindow: int = 5000, amount: str, isolated: bool = False, unsafe: bool = False) -> BorrowResponse | Error:
    params = {
      'asset': asset,
      'amount': amount,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
      'type': type,
    }
    if symbol:
      params['symbol'] = symbol
    if isolated:
      params['isIsolated'] = 'TRUE'
    query = self.signed_query(params)
    r = await self.client.post(
      f'{self.base}/sapi/v1/margin/borrow-repay?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, BorrowResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error fetching order: {val.code}, {val.msg}')
    return val
  



class _Data(UserMixin):
  ...