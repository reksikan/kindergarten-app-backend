from pydantic import BaseModel


class YawnSchema(BaseModel):
    class Config:
        from_attributes = True

    value: str
    id: int


class DefecationSchema(BaseModel):
    class Config:
        from_attributes = True

    value: str
    id: int


class SkinCoveringSchema(BaseModel):
    class Config:
        from_attributes = True

    value: str
    id: int
