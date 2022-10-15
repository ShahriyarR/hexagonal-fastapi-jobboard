from pydantic import BaseModel, EmailStr


# properties required during user creation
class UserInputDto(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserOutputDto(BaseModel):
    user_name: str
    email: EmailStr
    is_active: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
