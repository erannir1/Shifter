from typing import List
from pydantic import BaseModel

from modules.shift.shift import Shift
from modules.user.user import User


class TradeRequest(BaseModel):
    user: User
    exchanging_shifts: List[Shift]
    receiving_shifts: List[Shift] = None
