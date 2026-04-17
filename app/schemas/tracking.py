from pydantic import BaseModel
from typing import List, Dict, Union

class LiveTrackingRequest(BaseModel):
    form_id: str

class LiveTrackingResponse(BaseModel):
    message: str
    status: bool
    started:bool
    data: Union[List[Dict], None]

class NextCustomerRequest(BaseModel):
    form_id: str
    client_id: str

class NextCustomerResponse(BaseModel):
    message: str
    status: bool
    started: bool
