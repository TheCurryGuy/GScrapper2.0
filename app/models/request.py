from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuthorRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=200, description="Author's full name")
    email: EmailStr = Field(..., description="Author's email address")
    orcid_id: Optional[str] = Field(None, description="ORCID ID (if known)", pattern=r'^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$')
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@university.edu",
                "orcid_id": "0000-0001-2345-6789"
            }
        }
