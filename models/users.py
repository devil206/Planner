
from models.events import Event
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example":{
                "email": "fastapi@gmail.com",
                "password":"strong",
               

            }
        }



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
