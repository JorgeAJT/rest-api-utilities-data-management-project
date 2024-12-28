from typing import Union, Dict, List

from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    message: Union[str, Dict, List[Dict]]
