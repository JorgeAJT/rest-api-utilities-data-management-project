from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from .brand_enum import BrandEnum
from .energy_type_enum import EnergyTypeEnum


class MeterReadingsRequest(BaseModel):
    meter_number: str
    connection_ean_code: str
    account_id: str
    brand: BrandEnum
    energy_type: EnergyTypeEnum
    reading_date: date
    reading_electricity: Optional[str] = Field(default=None)
    reading_gas: Optional[str] = Field(default=None)
    rejection: Optional[str] = Field(default=None)
    validation_status: str


class MeterReadingsResponse(BaseModel):
    meter_readings_id: int
    meter_number: str
    connection_ean_code: str
    account_id: str
    brand: BrandEnum
    energy_type: EnergyTypeEnum
    reading_date: date
    reading_electricity: Optional[str] = Field(default=None)
    reading_gas: Optional[str] = Field(default=None)
    rejection: Optional[str] = Field(default=None)
    validation_status: str
