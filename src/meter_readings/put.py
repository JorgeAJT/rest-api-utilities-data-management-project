from fastapi import APIRouter

from src.models import Response, MeterReadingsResponse, MeterReadingsRequest
from src.utils import setup_logger, db_connection

logger = setup_logger('meter-readings-put')

meter_readings_put_router = APIRouter()


@meter_readings_put_router.put('/meter_readings/{meter_readings_id}')
async def put_meter_readings(meter_readings_id: int, meter_readings_request: MeterReadingsRequest) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM meter_readings WHERE meter_readings_id = %s', (meter_readings_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"No data found for meter_readings_id: {meter_readings_id}")
                    return Response(status_code=404, message="meter_readings_id not found in any meter_readings row")

                values_tuple = tuple(meter_readings_request.dict().values()) + (meter_readings_id,)
                cursor.execute("""
                    UPDATE meter_readings
                    SET meter_number = %s, 
                        connection_ean_code = %s, 
                        account_id = %s, 
                        brand = %s, 
                        energy_type = %s,
                        reading_date = %s, 
                        reading_electricity = %s, 
                        reading_gas = %s, 
                        rejection = %s, 
                        validation_status = %s
                    WHERE meter_readings_id = %s
                """, values_tuple)
                conn.commit()
                meter_readings_response = MeterReadingsResponse(meter_readings_id=meter_readings_id,
                                                                **meter_readings_request.dict())
                logger.info(f"Successfully updated in meter_readings: {meter_readings_response.dict()}")
                return Response(status_code=201, message={"meter_readings": meter_readings_response.dict()})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
