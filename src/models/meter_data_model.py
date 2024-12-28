from datetime import datetime

from pydantic import BaseModel

from .brand_enum_model import BrandEnum


class MeterDataRequest(BaseModel):
    meter_number: str
    connection_ean_code: str
    business_partner_id: str
    brand: BrandEnum
    grid_company_code: str
    oda_code: str
    smart_collectable: str
    sjv1: float
    sjv2: float
    installation: str
    division: str
    move_out_date: datetime
    row_create_datetime: datetime
    move_in_date: datetime


class MeterDataResponse(BaseModel):
    meter_data_id: int
    meter_number: str
    connection_ean_code: str
    business_partner_id: str
    brand: BrandEnum
    grid_company_code: str
    oda_code: str
    smart_collectable: str
    sjv1: float
    sjv2: float
    installation: str
    division: str
    move_out_date: datetime
    row_create_datetime: datetime
    move_in_date: datetime
