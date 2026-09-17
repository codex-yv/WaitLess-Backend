from pydantic import BaseModel
from typing import Union, List, Dict


class FormsResponse(BaseModel):
    message:str
    error:Union[str, None]
    data:Union[List[Dict], None]
    status:bool

class CreateFormRequest(BaseModel):
    form_params:List[Dict]
    title:str
    counter:str
    opens_at:str
    closes_at:str

class CreateFormResponse(BaseModel):    
    message:str
    form_id:str
    error:Union[str, None]
    status:bool

class SubmitFormRequest(BaseModel):
    form_id:str
    params_val:List[Dict]

class SubmitFormResponse(BaseModel):
    message:str
    error:Union[str, None]
    status:bool
    client_id:Union[str, None]
    access_token:Union[str, None]
    token_type:Union[str, None]

class DeleteFormResponse(BaseModel):
    message:str
    status: bool

class DeleteFormRequest(BaseModel):
    form_id: str