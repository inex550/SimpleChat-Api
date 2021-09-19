from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    username: str = Field(..., example='username')
    password: str = Field(..., example='password')


class Token(BaseModel):
    token: str = Field(..., example='<token>')

    class Config:
        orm_mode = True