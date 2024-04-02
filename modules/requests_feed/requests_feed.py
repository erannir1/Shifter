from typing import List
from pydantic import BaseModel

from modules.trade_request.trade_request import TradeRequest


class RequestsFeed(BaseModel):
    list_of_trade_requests: List[TradeRequest]
