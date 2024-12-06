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
    reading_electricity: str
    reading_gas: str
    rejection: str
    validation_status: str

class MeterReadingsResponse(BaseModel):
    meter_readings_id: int
    meter_number: str
    connection_ean_code: str
    account_id: str
    brand: BrandEnum
    energy_type: EnergyTypeEnum
    reading_date: date
    reading_electricity: str
    reading_gas: str
    rejection: str
    validation_status: str