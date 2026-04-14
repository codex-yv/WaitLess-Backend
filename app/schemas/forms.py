from pydantic import BaseModel
from typing import Union, List, Dict


class FormsResponse(BaseModel):
    message:str
    error:Union[str, None]
    data:Union[dict, None]
    status:bool

class CreateFormRequest(BaseModel):
    form_params:List[Dict[str, Dict[str, Union[str, int, None]]]]
    opens_at:str
    closes_at:str

class CreateFormResponse(BaseModel):    
    message:str
    form_id:str
    error:Union[str, None]
    status:bool