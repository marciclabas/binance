from typing_extensions import Literal, overload, TypeVar
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from binance.util import UserMixin, timestamp
from binance.types import OrderStatus, Error, Order, ListStatusType, ListOrderStatus, validate_response

T = TypeVar('T')

ReplaceMode = Literal['STOP_ON_FAILURE', 'ALLOW_FAILURE']

class Fill(BaseModel):
  price: str
  qty: str
  commission: str
  commissionAsset: str

class OrderResponse(BaseModel):
  orderId: int
  status: OrderStatus
  price: str
  fills: list[Fill] = []

class PartialOrder(BaseModel):
  symbol: str
  orderId: int

class ListOrderResponse(BaseModel):
  orderListId: int
  listStatusType: ListStatusType
  listOrderStatus: ListOrderStatus
  orders: list[PartialOrder]

@dataclass
class Spot(UserMixin):
  recvWindow: int = 5000

  @UserMixin.with_client
  async def query_order(self, symbol: str, orderId: int) -> OrderResponse | Error:
    """Query an Order"""
    query = self.signed_query({
      'symbol': symbol,
      'orderId': orderId,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })
    r = await self.client.get(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, OrderResponse)
  
  @UserMixin.with_client
  async def query_order_list(self, orderListId: int) -> ListOrderResponse | Error:
    query = self.signed_query({
      'orderListId': orderListId,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })
    r = await self.client.get(
      f'{self.base}/api/v3/orderList?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, ListOrderResponse)

  @UserMixin.with_client
  async def spot_order(self, pair: str, order: Order) -> OrderResponse | Error:
    query = self.signed_query({
      'symbol': pair,
      'timestamp': timestamp.now(),
      'newOrderRespType': 'FULL',
      **order,
    })
    r = await self.client.post(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, OrderResponse)
  
  @UserMixin.with_client
  async def oto_order(self, pair: str, *, working: Order, pending: Order) -> ListOrderResponse | Error:

    def cap_first(s: str):
      return s[0].upper() + s[1:]

    def rename(order: Order, prefix: str) -> dict:
      return {prefix + cap_first(key): value for key, value in order.items()}
    
    query = self.signed_query({
      'symbol': pair,
      'timestamp': timestamp.now(),
      'newOrderRespType': 'FULL',
      **rename(working, 'working'),
      **rename(pending, 'pending'),
    })
    r = await self.client.post(
      f'{self.base}/api/v3/orderList/oto?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, ListOrderResponse)


  @UserMixin.with_client
  async def replace_order(self, pair: str, orderId: int, order: Order) -> OrderResponse | Error:
    query = self.signed_query({
      'symbol': pair,
      'cancelOrderId': orderId,
      'newOrderRespType': 'FULL',
      'timestamp': timestamp.now(),
      **order,
    })
    r = await self.client.post(
      f'{self.base}/api/v3/order/cancelReplace?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, OrderResponse)
  

  @UserMixin.with_client
  async def cancel_order(self, symbol: str, orderId: int):
    query = self.signed_query({
      'symbol': symbol,
      'orderId': orderId,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })

    r = await self.client.delete(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    validate_response(r.text)
  
  
  @UserMixin.with_client
  async def cancel_order_list(self, symbol: str, orderListId: int) -> ListOrderResponse:
    query = self.signed_query({
      'symbol': symbol,
      'orderListId': orderListId,
      'recvWindow': self.recvWindow,
      'timestamp': timestamp.now(),
    })
    r = await self.client.delete(
      f'{self.base}/api/v3/orderList?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, ListOrderResponse)
  