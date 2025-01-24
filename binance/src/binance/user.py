from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, TypeAdapter
from binance.types import OrderStatus, Side
from binance.util import timestamp, UserMixin

class Balance(BaseModel):
  asset: str
  free: str
  locked: str

class BalanceResponse(BaseModel):
  balances: list[Balance]

  def free(self, asset: str) -> Decimal:
    for b in self.balances:
      if b.asset == asset:
        return Decimal(b.free)
    return Decimal(0)
  
@dataclass
class _Balance(UserMixin):
  recvWindow: int = 5000
  @UserMixin.with_client
  async def balance(self, omitZeroBalances: bool = True) -> BalanceResponse:
    query = self.signed_query({
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
      'omitZeroBalances': omitZeroBalances,
    })
    r = await self.client.get(
      f'{self.base}/api/v3/account?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return BalanceResponse.model_validate_json(r.text)
  

class Order(BaseModel):
  price: str
  side: Side
  orderId: int
  origQty: str
  status: OrderStatus

OrdersAdapter = TypeAdapter(list[Order])

@dataclass
class _Orders(UserMixin):
  recvWindow: int = 5000
  
  @UserMixin.with_client
  async def orders(self, symbol: str) -> list[Order]:
    query = self.signed_query({
      'symbol': symbol,
      'timestamp': timestamp.now(),
      'recvWindow': self.recvWindow,
    })
    r = await self.client.get(
      f'{self.base}/api/v3/allOrders?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return OrdersAdapter.validate_json(r.text)
  

@dataclass
class User(_Balance, _Orders):
  ...