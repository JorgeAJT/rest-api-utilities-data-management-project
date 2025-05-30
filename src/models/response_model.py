from typing import Union, Dict, List

from pydantic import BaseModel, ConfigDict


class Response(BaseModel):
    status_code: int
    message: Union[str, Dict, List[Dict]]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status_code": 200,
                "message": {
                    "table_name": [
                        {
                            "field1": "value1",
                            "field2": "value2",
                            "…": "…"
                        }
                    ]
                }
            }
        }
    )
