from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from src.utils import setup_logger, db_connection
from src.models import Response

logger = setup_logger('mandate-data-get')

try:
    conn = db_connection()
    mandate_data_get_router = APIRouter()

    @mandate_data_get_router.get('/mandate_data/{business_partner_id}', response_model=Response)
    async def get_mandate_data_by_path_params(business_partner_id: str):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('SELECT * FROM mandate_data WHERE business_partner_id = %s', (business_partner_id,))
            value = cursor.fetchall()

            if not value:
                logger.warning(f"No data found for business_partner_id: {business_partner_id}")
                return Response(status_code=404, message="business_partner_id not found in any mandate_data row")

            logger.info(f"Data successfully retrieved for business_partner_id: {business_partner_id}")
            return Response(status_code=200, message={"mandate_data": value})
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return Response(status_code=500, message="An internal error occurred while GET query in mandate_data")
        finally:
            cursor.close()

    @mandate_data_get_router.get('/mandate_data/', response_model=Response)
    async def get_mandate_data_by_query_params(
            business_partner_id: str,
            mandate_status: str,
            collection_frequency: str = None):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if collection_frequency:
                query = ('SELECT * FROM mandate_data WHERE business_partner_id = %s AND mandate_status = %s AND '
                         'collection_frequency = %s')
                params = (business_partner_id, mandate_status, collection_frequency)
            else:
                query = 'SELECT * FROM mandate_data WHERE business_partner_id = %s AND mandate_status = %s'
                params = (business_partner_id, mandate_status)
            cursor.execute(query, params)
            value = cursor.fetchall()

            if not value:
                logger.warning(f"No data found for business_partner_id: {business_partner_id}")
                return Response(status_code=404, message="mandate_data row not found")

            logger.info(f"Data successfully retrieved")
            return Response(status_code=200, message={"mandate_data": value})
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return Response(status_code=500, message="An internal error occurred while GET query in mandate_data")
        finally:
            cursor.close()

except Exception as e:
    logger.error(f"Error: {e}")
    raise e