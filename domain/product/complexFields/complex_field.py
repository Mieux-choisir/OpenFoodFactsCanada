from pydantic import field_validator, BaseModel


class ComplexField(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
