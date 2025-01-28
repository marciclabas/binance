from typing_extensions import TypeVar
from dataclasses import dataclass
from pydantic import BaseModel
from binance.user import UserMixin
from binance.util import timestamp
from binance.types import validate_response

M = TypeVar('M', bound=BaseModel)

class EarnPositionRow(BaseModel):
  totalAmount: str
  productId: str
  autoSubscribe: bool

class EarnPositionResponse(BaseModel):
  rows: list[EarnPositionRow]

class EarnSubscribeResponse(BaseModel):
  purchaseId: int
  success: bool
  amount: str
  
class EarnRedeemResponse(BaseModel):
  redeemId: int
  success: bool

@dataclass
class SimpleEarn(UserMixin):
  recvWindow: int = 5000
  @UserMixin.with_client
  async def position(self, asset: str) -> list[EarnPositionRow]:
    query = self.signed_query({
      'asset': asset,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })
    r = await self.client.get(
      f'{self.base}/sapi/v1/simple-earn/flexible/position?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, EarnPositionResponse).rows
  
  @UserMixin.with_client
  async def subscribe(self, *, productId: str, amount: str, auto_subscribe: bool = False) -> EarnSubscribeResponse:
    query = self.signed_query({
      'productId': productId,
      'amount': amount,
      'autoSubscribe': auto_subscribe,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })
    r = await self.client.post(
      f'{self.base}/sapi/v1/simple-earn/flexible/subscribe?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, EarnSubscribeResponse)
  
  @UserMixin.with_client
  async def redeem(self, *, productId: str, amount: str | None = None) -> EarnRedeemResponse:
    """Redeem flexible savings product. If `amount is None`, redeems all."""
    params = {
      'productId': productId,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
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
    return validate_response(r.text, EarnRedeemResponse)
