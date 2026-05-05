from pydantic import BaseModel
from typing import Union
class LoginRequest(BaseModel):
    email:str
    password:str

class LoginResponse(BaseModel):
    message:str
    status:bool
    email: Union[str, None]
    picture: Union[str, None] = None
    admin_id:Union[str, None]
    access_token:Union[str, None]
    token_type:Union[str, None]

class SignupRequest(BaseModel):
    name:str
    email:str
    password:str
    picture: str | None = None
    phone:str
    occupation:str
    org_type:str
    org_name:str
    address:str

class SignupResponse(BaseModel):
    message:str
    status:bool
    email: str | None = None
    picture: str | None = None
    admin_id:Union[str, None]
    access_token:Union[str, None]
    token_type:Union[str, None]


class CoordinatorLoginRequest(BaseModel):
    email:str
    token:str

class CoordinatorLoginResponse(BaseModel):
    message:str
    status:bool
    access_token:Union[str, None]
    token_type:Union[str, None]