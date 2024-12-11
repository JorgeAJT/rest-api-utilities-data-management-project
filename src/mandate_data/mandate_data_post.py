from fastapi import APIRouter
from src.utils import setup_logger, db_connection
from src.models import Response, MandateData

logger = setup_logger("mandate-data-post")

mandate_data_post_router = APIRouter()

@mandate_data_post_router.post('/mandate_data/', response_model=Response)
async def post_mandate_data(mandate_data: MandateData):
    with db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                values_tuple = tuple(mandate_data.dict().values())
                cursor.execute("""
                    INSERT INTO mandate_data (
                        mandate_id, business_partner_id, brand, mandate_status,
                        collection_frequency, row_update_datetime, row_create_datetime,
                        changed_by, collection_type, metering_consent
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, values_tuple)
                conn.commit()
                logger.info(f"Successfully inserted into mandate_data: {mandate_data.dict()}")
                return Response(status_code=201, message={"mandate_data": mandate_data.dict()})
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                return Response(status_code=400, message="mandate_data body wasn't correct")