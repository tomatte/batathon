from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Association table for many-to-many relationship between User and JobType
class UserJobTypeLink(SQLModel, table=True):
    __tablename__ = 'user_job_type'
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    job_type_id: Optional[int] = Field(default=None, foreign_key="job_types.id", primary_key=True)

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    phone: str = Field(nullable=False, unique=True)
    
    # Relationship with JobType through the association table
    willing_jobs: List["JobType"] = Relationship(
        back_populates="interested_users",
        link_model=UserJobTypeLink
    )

    def __repr__(self):
        return f"<User(name='{self.name}', phone='{self.phone}')>"

class JobType(SQLModel, table=True):
    __tablename__ = 'job_types'

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(nullable=False)
    
    # Relationship with User through the association table
    interested_users: List[User] = Relationship(
        back_populates="willing_jobs",
        link_model=UserJobTypeLink
    )

    def __repr__(self):
        return f"<JobType(description='{self.description}')>" 