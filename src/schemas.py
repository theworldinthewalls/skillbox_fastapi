from pydantic import BaseModel, ConfigDict


class Dish(BaseModel):
    name: str
    time: int


class Summary(Dish):
    views: int
    model_config = ConfigDict(from_attributes=True)


class RecipeCreate(Dish):
    ingredients: str
    description: str


class RecipeRead(RecipeCreate):
    model_config = ConfigDict(from_attributes=True)
