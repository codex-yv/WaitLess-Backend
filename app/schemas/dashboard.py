from pydantic import BaseModel
from typing import Union, Dict

class DashboardResponse(BaseModel):
    status:bool
    message:str
    data: Union[Dict[str, Union[int, str]], None]

class CoordinatorRequest(BaseModel):
    name:str
    email:str

class CoordinatorResponse(BaseModel):
    status:bool
    message:str