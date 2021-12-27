from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    username: str = Field(..., min_length=1, example='username')
    password: str = Field(..., min_length=1, example='password')


class UserIdentifers(BaseModel):
    id:         int
    token:      str = Field(...,  example='<token>')
    username:   str = Field(...,  example='Alex123')
    avatar:     str = Field(None, example='user.png')

    class Config:
        orm_mode = True