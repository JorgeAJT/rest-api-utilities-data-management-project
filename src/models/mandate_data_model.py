from pydantic import BaseModel
from datetime import datetime
from .brand_enum_model import BrandEnum

class MandateData(BaseModel):
    mandate_id: int
    business_partner_id: str
    brand: BrandEnum
    mandate_status: str
    collection_frequency: str
    row_update_datetime: datetime
    row_create_datetime: datetime
    changed_by: str
    collection_type: str
    metering_consent: str