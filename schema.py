from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


# globally validate the mobile numbers
class UserLogin(BaseModel):
    user_name: str = Field('Enter username')
    password: str = Field('Enter password')


class UserDetails(UserLogin):
    first_name: str = Field('Enter first name', pattern=r'^[A-Z]{1}\D{1,}$')
    last_name: str = Field('Enter last name', pattern=r'^[A-Z]{1}\D{1,}$')
    email: EmailStr = Field('Enter email')
    phone: int = Field('Enter phone number')
    city: str = Field('Enter city')
    state: str = Field('Enter state ')
    is_verified: Optional[bool] = Field(default=False)


class UserNotes(BaseModel):
    title: str = Field("Enter title ", pattern=r'^[A-Z]{1}\D{1,}')
    description: str
    color: str


class LabelSchema(BaseModel):
    label_name: str = Field('Field name')


class CollaboratorDetails(BaseModel):
    user_ids: List[int]
    note_id: int
