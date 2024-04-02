from typing import Dict, List

from pydantic import BaseModel


class Company(BaseModel):
    company_name: str
    roles: str
    qualifications: Dict[
        str, List[str]
    ]  # Key is a role value is a list of qualifications match the role
