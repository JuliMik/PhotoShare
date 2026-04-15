from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    hashed_password: str
    role: str
    is_active: bool
