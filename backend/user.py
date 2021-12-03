from pydantic import BaseModel


class user_token(BaseModel):
    client_id: str
    response_type: str
    redirect_uri: str
    scope: str
