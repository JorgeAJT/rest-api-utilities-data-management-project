from fastapi import APIRouter

from src.models import Response, MeterReadingsResponse, MeterReadingsRequest
from src.utils import setup_logger, db_connection

logger = setup_logger('meter-readings-post')

meter_readings_post_router = APIRouter()


@meter_readings_post_router.post('/meter_readings/')
async def post_meter_readings(meter_readings_request: MeterReadingsRequest) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                values_tuple = tuple(meter_readings_request.model_dump().values())
                cursor.execute("INSERT INTO meter_readings "
                               "(meter_number, connection_ean_code, account_id, brand, energy_type, "
                               "reading_date, reading_electricity, reading_gas, rejection, validation_status) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING meter_readings_id",
                               values_tuple)
                new_id = cursor.fetchone()[0]
                conn.commit()
                meter_readings_response = MeterReadingsResponse(meter_readings_id=new_id,
                                                                **meter_readings_request.model_dump())
                logger.info(f"Successfully inserted into meter_readings: {meter_readings_response.model_dump()}")
                return Response(status_code=201, message={"meter_readings": [meter_readings_response.model_dump()]})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
