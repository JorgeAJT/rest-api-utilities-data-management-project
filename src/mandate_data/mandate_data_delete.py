from fastapi import APIRouter
from src.utils import setup_logger, db_connection
from src.models import Response

logger = setup_logger('mandate-data-delete')

mandate_data_delete_router = APIRouter()

@mandate_data_delete_router.delete('/mandate_data/{mandate_id}', response_model=Response)
async def delete_mandate_data(mandate_id: int):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM mandate_data WHERE mandate_id = %s', (mandate_id,))
                value = cursor.fetchone()

                if not value:
                    logger.warning(f"No data found for mandate_id: {mandate_id}")
                    return Response(status_code=404, message="mandate_id not found in any mandate_data row")

                cursor.execute('DELETE FROM mandate_data WHERE mandate_id = %s', (mandate_id,))
                conn.commit()
                logger.info(f"mandate_data row with mandate_id {mandate_id} deleted successfully")
                return Response(status_code=200,
                                message=f"mandate_data row with mandate_id {mandate_id} deleted successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")