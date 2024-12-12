from fastapi import APIRouter
from src.utils import setup_logger, db_connection
from src.models import Response, MeterDataResponse, MeterDataRequest

logger = setup_logger('meter-data-put')

meter_data_put_router = APIRouter()

@meter_data_put_router.put('/meter_data/{meter_data_id}', response_model=Response)
async def put_meter_data(meter_data_id: int, meter_data_request: MeterDataRequest):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                values_tuple = tuple(meter_data_request.dict().values()) + (meter_data_id,)
                cursor.execute("""
                    UPDATE meter_data 
                    SET meter_number = %s, 
                        connection_ean_code = %s, 
                        business_partner_id = %s, 
                        brand = %s,
                        grid_company_code = %s, 
                        oda_code = %s, 
                        smart_collectable = %s,
                        sjv1 = %s, 
                        sjv2 = %s, 
                        installation = %s,
                        division = %s,
                        move_out_date = %s,
                        row_create_datetime = %s,
                        move_in_date = %s
                    WHERE meter_data_id = %s
                """, values_tuple)
                conn.commit()
                meter_data_response = MeterDataResponse(meter_data_id=meter_data_id, **meter_data_request.dict())
                logger.info(f"Successfully updated in meter_data: {meter_data_response.dict()}")
                return Response(status_code=201, message={"meter_data": meter_data_response.dict()})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")