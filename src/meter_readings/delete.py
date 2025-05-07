from fastapi import APIRouter

from src.models import Response
from src.utils import setup_logger, db_connection, COMMON_RESPONSES_DELETE

logger = setup_logger('meter-readings-delete')

meter_readings_delete_router = APIRouter(
  prefix="/meter_readings",
  tags=["meter_readings"],
)


@meter_readings_delete_router.delete(
    '/{meter_readings_id}',
    response_model=Response,
    responses=COMMON_RESPONSES_DELETE
)
async def delete_meter_readings(meter_readings_id: int) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM meter_readings WHERE meter_readings_id = %s', (meter_readings_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"Data not found for meter_readings_id: {meter_readings_id}")
                    return Response(status_code=404, message="meter_readings_id not found in any meter_readings row")

                cursor.execute('DELETE FROM meter_readings WHERE meter_readings_id = %s', (meter_readings_id,))
                conn.commit()
                logger.info(f"meter_readings row with meter_readings_id {meter_readings_id} deleted successfully")
                return Response(status_code=200,
                                message=f"meter_readings row with meter_readings_id {meter_readings_id} "
                                        f"deleted successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
