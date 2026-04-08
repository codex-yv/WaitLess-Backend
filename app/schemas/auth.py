from pydantic import BaseModel
from typing import Union
class LoginRequest(BaseModel):
    email:str
    password:str

class LoginResponse(BaseModel):
    message:str
    status:bool
    access_token:Union[str, None]
    token_type:Union[str, None]

class SignupRequest(BaseModel):
    name:str
    email:str
    password:str
    phone:str
    occupation:str

class SignupResponse(BaseModel):
    message:str
    status:bool
    access_token:Union[str, None]
    token_type:Union[str, None]