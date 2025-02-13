from dataclasses import dataclass
from .trading import Trading
from .leasing import Leasing

@dataclass
class Margin(Trading, Leasing):
  ...