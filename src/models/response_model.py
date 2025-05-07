from typing import Union, Dict, List

from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    message: Union[str, Dict, List[Dict]]

    class Config:
        schema_extra = {
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
