from pydantic import BaseModel, Field

class register(BaseModel):
    firstname: str = Field(..., min_length=2)
    lastname: str = Field(..., min_length=2)
    email: str = Field(..., pattern=r".+@gmail\.com$")
    password: str = Field(..., min_length=8)
    confirmPassword: str = Field(..., min_length=8)


class login(BaseModel):
    email: str = Field(..., pattern=r".+@gmail\.com$")
    password: str = Field(..., min_length=8)


class response(BaseModel):
    name:str