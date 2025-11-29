from pydantic import BaseModel, Field
from typing import Optional, List

class UserModel(BaseModel):
    user_id: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: List[str] = Field(default_factory=list)
    emergency_contact: Optional[str] = None