from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class JobBase(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = "Remote"
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()
    is_active: Optional[bool] = True


# this will be used to validate data while creating a Job
class JobCreateInputDto(JobBase):
    title: str
    company: str
    location: str
    description: str

    class Config:
        orm_mode = True


# this will be used to format the response to not have id,owner_id etc
class JobOutputDto(JobBase):
    id: int
    title: str
    company: str
    company_url: Optional[str]
    location: str
    date_posted: date
    description: Optional[str]
    owner_id: int

    class Config:  # to convert non dict obj to json
        orm_mode = True
