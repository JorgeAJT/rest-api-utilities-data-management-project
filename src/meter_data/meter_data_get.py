from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from src.utils import setup_logger, db_connection
from src.models import Response

logger = setup_logger('meter-data-get')

meter_data_get_router = APIRouter()

@meter_data_get_router.get('/meter_data/{connection_ean_code}', response_model=Response)
async def get_meter_data_by_path_params_connection_ean_code(connection_ean_code: str):
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE connection_ean_code = %s', (connection_ean_code,))
                value = cursor.fetchall()

                if not value:
                    logger.warning(f"No data found for connection_ean_code: {connection_ean_code}")
                    return Response(status_code=404, message="connection_ean_code not found in any meter_data row")

                logger.info(f"Data successfully retrieved for connection_ean_code: {connection_ean_code}")
                return Response(status_code=200, message={"meter_data": value})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")

@meter_data_get_router.get('/meter_data/', response_model=Response)
async def get_meter_data_by_query_params_business_partner_id(business_partner_id: str):
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE business_partner_id = %s', (business_partner_id,))
                value = cursor.fetchall()

                if not value:
                    logger.warning(f"No data found for business_partner_id: {business_partner_id}")
                    return Response(status_code=404, message="business_partner_id not found in any meter_data row")

                logger.info(f"Data successfully retrieved for business_partner_id: {business_partner_id}")
                return Response(status_code=200, message={"meter_data": value})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")

@meter_data_get_router.get('/meter_data/', response_model=Response)
async def get_meter_data_by_some_query_params(
        business_partner_id: str,
        connection_ean_code: str):
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM meter_data WHERE business_partner_id = %s AND connection_ean_code = %s',
                               (business_partner_id, connection_ean_code))
                value = cursor.fetchall()

                if not value:
                    logger.warning(f"No data found for this request")
                    return Response(status_code=404, message="meter_data row not found")

                logger.info(f"Data successfully retrieved")
                return Response(status_code=200, message={"meter_data": value})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")

