from pydantic import BaseModel
from typing import Optional

class GameInput(BaseModel):
    username: str
    game_name: str
    is_finished: Optional[bool] = False

class DeleteGameRequest(BaseModel):
    game_name: str
    username: str

class GameStatusUpdate(BaseModel):
    game_name: str
    username: str
    
class GameQuery(BaseModel):
    username: str
