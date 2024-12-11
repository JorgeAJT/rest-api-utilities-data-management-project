from fastapi import APIRouter
from src.utils import setup_logger, db_connection
from src.models import Response, MandateData

logger = setup_logger("mandate-data-put")

mandate_data_put_router = APIRouter()

@mandate_data_put_router.put('/mandate_data/{mandate_id}', response_model=Response)
async def put_mandate_data(mandate_id: int, mandate_data: MandateData):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                values_tuple = tuple(mandate_data.dict().values()) + (mandate_id,)
                cursor.execute("""
                    UPDATE mandate_data 
                    SET mandate_id = %s, 
                        business_partner_id = %s, 
                        brand = %s, 
                        mandate_status = %s,
                        collection_frequency = %s, 
                        row_update_datetime = %s, 
                        row_create_datetime = %s,
                        changed_by = %s, 
                        collection_type = %s, 
                        metering_consent = %s
                    WHERE mandate_id = %s
                """, values_tuple)
                conn.commit()
                logger.info(f"Successfully updated in mandate_data: {mandate_data.dict()}")
                return Response(status_code=201, message={"mandate_data": mandate_data.dict()})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")