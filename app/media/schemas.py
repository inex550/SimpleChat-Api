from pydantic import BaseModel
from pydantic.fields import Field


class UploadedFile(BaseModel):
    name: str = Field(..., title="Name of uploaded file")