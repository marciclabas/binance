from typing_extensions import overload, Literal, TypeVar
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from binance.user import UserMixin
from binance.util import binance_timestamp, validate_response
from binance.types import Error

M = TypeVar('M', bound=BaseModel)

class EarnPositionRow(BaseModel):
  totalAmount: str
  productId: str
  autoSubscribe: bool

class EarnPositionResponse(BaseModel):
  rows: list[EarnPositionRow]
  code: Literal[None] = None

class EarnSubscribeResponse(BaseModel):
  purchaseId: int
  success: bool
  amount: str
  code: Literal[None] = None
  
class EarnRedeemResponse(BaseModel):
  redeemId: int
  success: bool
  code: Literal[None] = None


@dataclass
class SimpleEarn(UserMixin):
  @overload
  async def position(self, asset: str, *, recvWindow: int = 5000, unsafe: Literal[False] = False) -> list[EarnPositionRow] | Error:
    ...
  @overload
  async def position(self, asset: str, *, recvWindow: int = 5000, unsafe: Literal[True]) -> list[EarnPositionRow]:
    ...
  @UserMixin.with_client
  async def position(self, asset: str, *, recvWindow: int = 5000, unsafe: bool = False) -> list[EarnPositionRow] | Error:
    query = self.signed_query({
      'asset': asset,
      'recvWindow': recvWindow,
      'timestamp': binance_timestamp(datetime.now()),
    })
    r = await self.client.get(
      f'{self.base}/sapi/v1/simple-earn/flexible/position?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, EarnPositionResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error canceling order: {val.code}, {val.msg}')
    
    return val.rows if val.code is None else val
  

  @overload
  async def subscribe(self, *, productId: str, amount: str, auto_subscribe: bool = False, recvWindow: int = 5000, unsafe: Literal[False] = False) -> EarnSubscribeResponse | Error:
    ...
  @overload
  async def subscribe(self, *, productId: str, amount: str, auto_subscribe: bool = False, recvWindow: int = 5000, unsafe: Literal[True]) -> EarnSubscribeResponse:
    ...
  @UserMixin.with_client
  async def subscribe(self, *, productId: str, amount: str, auto_subscribe: bool = False, recvWindow: int = 5000, unsafe: bool = False) -> EarnSubscribeResponse | Error:
    query = self.signed_query({
      'productId': productId,
      'amount': amount,
      'autoSubscribe': auto_subscribe,
      'recvWindow': recvWindow,
      'timestamp': binance_timestamp(datetime.now()),
    })
    r = await self.client.post(
      f'{self.base}/sapi/v1/simple-earn/flexible/subscribe?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, EarnSubscribeResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error canceling order: {val.code}, {val.msg}')
    return val
  

  @overload
  async def redeem(self, *, productId: str, amount: str | None = None, recvWindow: int = 5000, unsafe: Literal[False] = False) -> EarnRedeemResponse | Error:
    ...
  @overload
  async def redeem(self, *, productId: str, amount: str | None = None, recvWindow: int = 5000, unsafe: Literal[True]) -> EarnRedeemResponse:
    ...
  @UserMixin.with_client
  async def redeem(self, *, productId: str, amount: str | None = None, recvWindow: int = 5000, unsafe: bool = False) -> EarnRedeemResponse | Error:
    params = {
      'productId': productId,
      'recvWindow': recvWindow,
      'timestamp': binance_timestamp(datetime.now()),
    }
    if amount is not None:
      params['amount'] = amount
    else:
      params['redeemAll'] = True
    query = self.signed_query(params)
    r = await self.client.post(
      f'{self.base}/sapi/v1/simple-earn/flexible/redeem?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, EarnRedeemResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error canceling order: {val.code}, {val.msg}')
    return val
