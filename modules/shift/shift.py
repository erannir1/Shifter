from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, AfterValidator


class Shift(BaseModel):
    qualification: str
    start_time: Annotated[datetime, AfterValidator(lambda v: v.isoformat())]
    end_time: Annotated[datetime, AfterValidator(lambda v: v.isoformat())]
