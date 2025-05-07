from fastapi import APIRouter
from psycopg2.extras import RealDictCursor

from src.models import Response
from src.utils import setup_logger, db_connection, COMMON_RESPONSES_GENERIC

logger = setup_logger('meter-data-get')

meter_data_get_router = APIRouter(
  prefix="/meter_data",
  tags=["meter_data"],
)


@meter_data_get_router.get(
    '/{connection_ean_code}',
    response_model=Response,
    responses=COMMON_RESPONSES_GENERIC
)
async def get_meter_data_by_path_params(connection_ean_code: str) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE connection_ean_code = %s', (connection_ean_code,))
                value = cursor.fetchall()

                if not value:
                    logger.warning(f"Data not found for connection_ean_code: {connection_ean_code}")
                    return Response(status_code=404, message="connection_ean_code not found in any meter_data row")

                logger.info(f"Data successfully retrieved for connection_ean_code: {connection_ean_code}")
                return Response(status_code=200, message={"meter_data": value})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")


@meter_data_get_router.get(
    '/',
    response_model=Response,
    responses=COMMON_RESPONSES_GENERIC
)
async def get_meter_data_by_query_params(
        business_partner_id: str = None,
        connection_ean_code: str = None) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if business_partner_id and connection_ean_code:
                    query = 'SELECT * FROM meter_data WHERE business_partner_id = %s AND connection_ean_code = %s'
                    params = (business_partner_id, connection_ean_code)
                elif business_partner_id:
                    query = 'SELECT * FROM meter_data WHERE business_partner_id = %s'
                    params = (business_partner_id,)
                elif connection_ean_code:
                    query = 'SELECT * FROM meter_data WHERE connection_ean_code = %s'
                    params = (connection_ean_code,)
                else:
                    logger.warning("No query parameters provided")
                    return Response(status_code=400, message="No query parameters provided")

                cursor.execute(query, params)
                value = cursor.fetchall()

                if not value:
                    logger.warning("Data not found for this request")
                    return Response(status_code=404, message="meter_data row not found")

                logger.info(f"Data successfully retrieved")
                return Response(status_code=200, message={"meter_data": value})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
