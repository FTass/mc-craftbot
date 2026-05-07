from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request accepted by POST /chat.

    The backend accepts both `message` and `question` to make the contract robust while
    the frontend is being connected. The recommended frontend field is `message`.
    """

    message: Optional[str] = Field(default=None, description="User message sent from the frontend.")
    question: Optional[str] = Field(default=None, description="Compatibility alias for message.")

    def text(self) -> str:
        return (self.message or self.question or "").strip()


class Ingredient(BaseModel):
    item: str
    quantity: int | float
    unit: Optional[str] = None


class Recipe(BaseModel):
    id: str
    name: str
    aliases: list[str] = []
    category: str
    station: str
    ingredients: list[Ingredient]
    grid: list[list[Optional[str]]]
    steps: list[str]
    usage: str
    notes: Optional[str] = None


class ChatResponse(BaseModel):
    status: str = Field(description="answered, not_found or error")
    answer: str
    matched_item: Optional[str] = None
    matched_recipe_id: Optional[str] = None
    source: str = "recipes.json"
    suggestions: list[str] = []


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    recipes_loaded: int
    ollama_model: str
    ollama_checked: bool = False
    ollama_available: Optional[bool] = None
