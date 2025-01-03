from typing_extensions import AsyncIterable, Generic, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_FLOOR
import json
import orjson
from pydantic import BaseModel, ValidationError
from urllib.parse import quote
from haskellian import ManagedAsync
from binance.types import Error, ErrorRoot

T = TypeVar('T')
M = TypeVar('M', bound=BaseModel)

def validate_response(r: str, Model: type[M]) -> M | Error:
  obj = orjson.loads(r)
  try:
    if 'code' in obj:
      return ErrorRoot.model_validate(obj).root
    return Model.model_validate(obj)
  except ValidationError as e:
    print('Error validating:', obj)
    raise e

def binance_timestamp(dt: datetime) -> int:
  return int(1e3*dt.timestamp())

def round2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).quantize(Decimal('1.'), rounding=ROUND_HALF_DOWN) * tick_size
  return r.normalize()

def trunc2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).to_integral_value(rounding=ROUND_FLOOR) * tick_size
  return r.normalize()

def sign(query_string: str, *, secret: str) -> str:
  import hmac
  import hashlib
  return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def encode_query(obj) -> str:
  return quote(json.dumps(obj, separators=(',', ':'))) # binance can't cope with spaces, it seems

@dataclass
class Stream(Generic[T]):
  stream: AsyncIterable[T]
  subscribers: list[ManagedAsync[T]] = field(default_factory=list)

  async def run(self):
    async for item in self.stream:
      for subscriber in self.subscribers:
        subscriber.push(item)

  def subscribe(self) -> ManagedAsync[T]:
    sub = ManagedAsync[T]()
    self.subscribers.append(sub)
    return sub