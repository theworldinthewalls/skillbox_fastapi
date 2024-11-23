from contextlib import asynccontextmanager
from typing import Dict, List, Union

from fastapi import FastAPI, HTTPException
from sqlalchemy import desc, update
from sqlalchemy.future import select

from src.database import engine, session
from src.models import Base, Recipe
from src.schemas import RecipeCreate, RecipeRead, Summary


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/recipes", response_model=List[Summary])
async def get_recipes() -> List[Summary]:
    result = await session.execute(
        select(Recipe.name, Recipe.time, Recipe.views).order_by(
            desc(Recipe.views), Recipe.time
        )
    )
    return [Summary.model_validate(row) for row in result.all()]


@app.get("/recipes/<int:id>", response_model=Union[RecipeRead | Dict])
async def get_recipe(recipe_id: int):
    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.one_or_none()
    if recipe:
        views = {"views": recipe[0].views + 1}
        await session.execute(
            update(Recipe).where(Recipe.id == recipe_id).values(views)
        )
        return recipe[0]
    else:
        raise HTTPException(
            status_code=404, detail="The server can't find the requested resource"
        )


@app.post("/recipes", response_model=RecipeRead)
async def add_recipe(data: RecipeCreate) -> Recipe:
    recipe = Recipe(**data.model_dump())
    async with session:
        session.add(recipe)
    return recipe
