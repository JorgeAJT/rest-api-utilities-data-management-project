from fastapi import APIRouter

from src.models import Response, MandateData
from src.utils import setup_logger, db_connection, COMMON_RESPONSES_GENERIC

logger = setup_logger('mandate-data-put')

mandate_data_put_router = APIRouter(
  prefix="/mandate_data",
  tags=["mandate_data"],
)


@mandate_data_put_router.put(
    '/{mandate_id}',
    response_model=Response,
    responses=COMMON_RESPONSES_GENERIC
)
async def put_mandate_data(mandate_id: int, mandate_data: MandateData) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM mandate_data WHERE mandate_id = %s', (mandate_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"Data not found for mandate_id: {mandate_id}")
                    return Response(status_code=404, message="mandate_id not found in any mandate_data row")

                values_tuple = tuple(mandate_data.model_dump().values()) + (mandate_id,)
                cursor.execute("UPDATE mandate_data "
                               "SET mandate_id = %s, "
                               "business_partner_id = %s, "
                               "brand = %s, mandate_status = %s, "
                               "collection_frequency = %s, "
                               "row_update_datetime = %s, "
                               "row_create_datetime = %s, "
                               "changed_by = %s, "
                               "collection_type = %s, "
                               "metering_consent = %s "
                               "WHERE mandate_id = %s",
                               values_tuple)
                conn.commit()
                logger.info(f"Successfully updated in mandate_data: {mandate_data.model_dump()}")
                return Response(status_code=201, message={"mandate_data": [mandate_data.model_dump()]})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
