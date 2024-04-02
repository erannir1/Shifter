from pydantic import BaseModel
from datetime import datetime


class Shift(BaseModel):
    qualification: str
    start_time: datetime
    end_time: datetime
