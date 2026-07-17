from pydantic import BaseModel


class StaffBase(BaseModel):
    full_name: str
    position: str
    phone: str | None = None
    email: str | None = None


class StaffCreate(StaffBase):
    pass


class StaffUpdate(StaffBase):
    pass


class StaffResponse(StaffBase):
    id: int

    class Config:
        from_attributes = True
