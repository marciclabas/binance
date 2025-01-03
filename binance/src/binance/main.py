from dataclasses import dataclass
from binance import Spot, Public, UserStream, User, SimpleEarn
from binance.user import UserMixin

@dataclass
class Binance(UserMixin):
  def __post_init__(self):
    self.spot = Spot(self.api_key, self.api_secret)
    self.public = Public()
    self.user_stream = UserStream(self.api_key, self.api_secret)
    self.user = User(self.api_key, self.api_secret)
    self.simple_earn = SimpleEarn(self.api_key, self.api_secret)
  
  @classmethod
  def env(cls):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    errs = []
    if (api_key := os.getenv('API_KEY')) is None:
      errs.append('API_KEY is not set')
    if (api_secret := os.getenv('API_SECRET')) is None:
      errs.append('API_SECRET is not set')
    if errs:
      raise RuntimeError(', '.join(errs))
    return cls(api_key, api_secret) # type: ignore