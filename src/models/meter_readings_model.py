from pydantic import BaseModel
from datetime import date
from .brand_enum_model import BrandEnum
from .energy_type_enum import EnergyTypeEnum

class MeterReadingsRequest(BaseModel):
    meter_number: str
    connection_ean_code: str
    account_id: str
    brand: BrandEnum
    energy_type: EnergyTypeEnum
    reading_date: date
    reading_electricity: str | None
    reading_gas: str | None
    rejection: str | None
    validation_status: str

class MeterReadingsResponse(BaseModel):
    meter_readings_id: int
    meter_number: str
    connection_ean_code: str
    account_id: str
    brand: BrandEnum
    energy_type: EnergyTypeEnum
    reading_date: date
    reading_electricity: str | None
    reading_gas: str | None
    rejection: str | None
    validation_status: str