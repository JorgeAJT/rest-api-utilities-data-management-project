from src.models import Response

SUCCESS_EXAMPLE_GENERIC = Response.model_config["json_schema_extra"]["example"]

SUCCESS_EXAMPLE_DELETE = {
    "status_code": 200,
    "message": "Row deleted successfully"
}

COMMON_RESPONSES_GENERIC = {
    200: {
        "model": Response,
        "description": "Successful operation",
        "content": {
            "application/json": {
                "example": SUCCESS_EXAMPLE_GENERIC
            }
        },
    },
    404: {
        "model": Response,
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 404,
                    "message": "Resource not found"
                }
            }
        }
    },
    500: {
        "model": Response,
        "description": "Internal error",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 500,
                    "message": "An internal error occurred while processing the request"
                }
            }
        }
    }
}

COMMON_RESPONSES_DELETE = {
    200: {
        "model": Response,
        "description": "Successful operation",
        "content": {
            "application/json": {
                "example": SUCCESS_EXAMPLE_DELETE
            }
        },
    },
    404: COMMON_RESPONSES_GENERIC[404],
    500: COMMON_RESPONSES_GENERIC[500]
}
