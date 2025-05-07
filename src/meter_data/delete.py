from fastapi import APIRouter

from src.models import Response
from src.utils import setup_logger, db_connection, COMMON_RESPONSES_DELETE

logger = setup_logger('meter-data-delete')

meter_data_delete_router = APIRouter(
  prefix="/meter_data",
  tags=["meter_data"],
)


@meter_data_delete_router.delete(
    '/{meter_data_id}',
    response_model=Response,
    responses=COMMON_RESPONSES_DELETE
)
async def delete_meter_data(meter_data_id: int) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE meter_data_id = %s', (meter_data_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"No data found for meter_data_id: {meter_data_id}")
                    return Response(status_code=404, message="meter_data_id not found in any meter_data row")

                cursor.execute('DELETE FROM meter_data WHERE meter_data_id = %s', (meter_data_id,))
                conn.commit()
                logger.info(f"meter_data row with meter_data_id {meter_data_id} deleted successfully")
                return Response(status_code=200,
                                message=f"meter_data row with meter_data_id {meter_data_id} deleted successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
