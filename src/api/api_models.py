from pydantic import BaseModel
from typing import Optional, Dict, List


class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class CourseDeletePydantic(BaseModel):
    name: str
    cid: Optional[str] = None
    semester: str

class updateUser(BaseModel):
    name:str
    sessionID:str
    email:str
    phone:str
    newPassword:str
    major:str
    degree:str

class UserPydantic(BaseModel):
     name: str
     email: str
     phone: str
     password: str
     major: str
     degree: str

class UserDeletePydantic(BaseModel):
    sessionID: str
    password: str

class UserCoursePydantic(BaseModel):
    name: str
    semester: str
    cid: str

class SubsemesterPydantic(BaseModel):
    semester: Optional[str] = None

class DefaultSemesterSetPydantic(BaseModel):
    default: str

class PickMultiple(BaseModel):
    pick: int
    classes: List[str]
    
class TemplatePydantic(BaseModel):
    year: int
    major: str
    school: str
    credits: int
    focus_track: bool
    link: str
    notes: List[str]
    required: List[str]
    pick_multiple: Dict[str, PickMultiple]

    classes: Dict[str, str]


    
