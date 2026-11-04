from datetime import datetime
from pydantic import BaseModel
from typing import List

class ErrorDetail(BaseModel):
    field:str
    issue:str 

class ErrorResponse(BaseModel):
    timestamp:str
    status:int
    error:str
    message:str
    path:str
    details:List[ErrorDetail] 