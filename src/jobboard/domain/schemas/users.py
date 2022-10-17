from pydantic import BaseModel, EmailStr


# properties required during user creation
class UserCreateInputDto(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserLoginInputDto(BaseModel):
    email: EmailStr
    password: str


class UserOutputDto(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    is_active: bool
    is_super_user: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
