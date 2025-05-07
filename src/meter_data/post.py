from fastapi import APIRouter

from src.models import Response, MeterDataResponse, MeterDataRequest
from src.utils import setup_logger, db_connection, COMMON_RESPONSES_GENERIC

logger = setup_logger('meter-data-post')

meter_data_post_router = APIRouter(
    prefix="/meter_data",
    tags=["meter_data"],
)


@meter_data_post_router.post(
    '/',
    response_model=Response,
    responses=COMMON_RESPONSES_GENERIC
)
async def post_meter_data(meter_data_request: MeterDataRequest) -> Response:
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                values_tuple = tuple(meter_data_request.model_dump().values())
                cursor.execute("INSERT INTO meter_data "
                               "(meter_number, connection_ean_code, business_partner_id, brand, "
                               "grid_company_code, oda_code, smart_collectable, sjv1, sjv2, installation, "
                               "division, move_out_date, row_create_datetime, move_in_date) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                               "RETURNING meter_data_id",
                               values_tuple)
                new_id = cursor.fetchone()[0]
                conn.commit()
                meter_data_response = MeterDataResponse(meter_data_id=new_id, **meter_data_request.model_dump())
                logger.info(f"Successfully inserted into meter_data: {meter_data_response.model_dump()}")
                return Response(status_code=201, message={"meter_data": [meter_data_response.model_dump()]})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=500, message="An internal error occurred while processing the request")
