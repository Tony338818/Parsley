from pydantic import BaseModel

class register(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    confirmPassword: str


class login(BaseModel):
    email: str
    password: str


class response(BaseModel):
    name:str