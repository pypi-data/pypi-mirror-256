from pydantic import BaseModel

class AllowedMethodsResponse(BaseModel):
    allowed_methods: list[str] 