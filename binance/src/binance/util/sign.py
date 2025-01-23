from dataclasses import dataclass
from urllib.parse import urlencode, quote
from .client import ClientMixin

def sign(query_string: str, *, secret: str) -> str:
  import hmac
  import hashlib
  return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def encode_query(obj) -> str:
  import json
  return quote(json.dumps(obj, separators=(',', ':'))) # binance can't cope with spaces, it seems

@dataclass
class UserMixin(ClientMixin):
  api_key: str
  api_secret: str
  base: str = 'https://api.binance.com'

  def sign(self, query_string: str) -> str:
    return sign(query_string, secret=self.api_secret)
  
  def signed_query(self, params: dict) -> str:
    query = urlencode(params)
    return query + '&signature=' + self.sign(query)