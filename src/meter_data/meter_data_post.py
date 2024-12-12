from fastapi import APIRouter
from src.utils import setup_logger, db_connection
from src.models import Response, MeterDataResponse, MeterDataRequest

logger = setup_logger('meter-data-post')

meter_data_post_router = APIRouter()

@meter_data_post_router.post('/meter_data/', response_model=Response)
async def post_meter_data(meter_data_request: MeterDataRequest):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                values_tuple = tuple(meter_data_request.dict().values())
                cursor.execute("""
                    INSERT INTO meter_data (
                        meter_number, connection_ean_code,business_partner_id, brand, grid_company_code,
                        oda_code, smart_collectable, sjv1, sjv2, installation, division,
                        move_out_date, row_create_datetime, move_in_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING meter_data_id
                """, values_tuple)
                new_id = cursor.fetchone()[0]
                conn.commit()
                meter_data_response = MeterDataResponse(meter_data_id=new_id, **meter_data_request.dict())
                logger.info(f"Successfully inserted into meter_data: {meter_data_response.dict()}")
                return Response(status_code=201, message={"meter_data": meter_data_response.dict()})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")