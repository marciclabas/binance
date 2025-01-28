from dataclasses import dataclass
from ._flexible_subscribe import _FlexibleSubscribe
from ._flexible_redeem import _FlexibleRedeem

@dataclass
class Earn(_FlexibleSubscribe, _FlexibleRedeem):
  ...