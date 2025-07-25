from __future__ import annotations
from pydantic import BaseModel,Field,validator
from uuid import UUID,uuid4

class Airport(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(...,min_length=3,max_length=180)
    iata_code: str = Field(...,min_length=3,max_length=3,description="IATA code,3 chars")
    city: str = Field(...,min_length=2)
    country: str = Field(...,min_length=2)

    @validator("iata_code")
    def uppercase_iata(cls, v: str):
        code = v.strip().upper()
        if not code.isalpha():
            raise ValueError("IATA code must consist of letters")
        return code

class AirportCreate(BaseModel):
    name: str
    iata_code: str
    city: str
    country: str

class AirportRead(Airport):
    pass