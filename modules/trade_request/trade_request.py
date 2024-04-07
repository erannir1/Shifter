from typing import List
from pydantic import BaseModel

from modules.shift.shift import Shift


class TradeRequest(BaseModel):
    company: str
    role: str
    exchanging_shifts: List[Shift]
    receiving_shifts: List[Shift] = None
