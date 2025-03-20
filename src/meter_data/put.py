from fastapi import APIRouter

from src.models import Response, MeterDataResponse, MeterDataRequest
from src.utils import setup_logger, db_connection

logger = setup_logger('meter-data-put')

meter_data_put_router = APIRouter()


@meter_data_put_router.put('/meter_data/{meter_data_id}')
async def put_meter_data(meter_data_id: int, meter_data_request: MeterDataRequest) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE meter_data_id = %s', (meter_data_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"No data found for meter_data_id: {meter_data_id}")
                    return Response(status_code=404, message="meter_data_id not found in any meter_data row")

                values_tuple = tuple(meter_data_request.model_dump().values()) + (meter_data_id,)
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
                meter_data_response = MeterDataResponse(meter_data_id=meter_data_id, **meter_data_request.model_dump())
                logger.info(f"Successfully updated in meter_data: {meter_data_response.model_dump()}")
                return Response(status_code=201, message={"meter_data": meter_data_response.model_dump()})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
