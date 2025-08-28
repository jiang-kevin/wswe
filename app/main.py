from contextlib import asynccontextmanager
from typing import Annotated, Sequence

from fastapi import FastAPI, Depends, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import Database
from models import Restaurant, RestaurantCreate, RestaurantPublicWithTags, Tag, TagBase, TagCreate, TagPublic

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create()
    yield

app = FastAPI(lifespan=lifespan, root_path="/api/v1")
SessionDep = Annotated[Session, Depends(db.session)]

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/restaurants", response_model=list[RestaurantPublicWithTags])
async def get_restaurants(session: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)):
    restaurants = session.exec(select(Restaurant).offset(offset).limit(limit)).all()
    return restaurants

@app.get("/restaurants/{id}")
async def get_restaurant_by_id(restaurant_id: int, session: SessionDep) -> Restaurant:
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    return restaurant

@app.post("/restaurants")
async def create_restaurant(restaurant: Annotated[RestaurantCreate, Form()], session: SessionDep) -> Restaurant:
    db_tags = session.exec(select(Tag).where(Tag.id in restaurant.tag_ids)).all()
    db_restaurant = Restaurant.model_validate(restaurant)
    db_restaurant.tags = list(db_tags)
    session.add(db_restaurant)
    session.commit()
    session.refresh(db_restaurant)
    return db_restaurant

@app.get("/tags")
async def get_tags(session: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)) -> Sequence[Tag]:
    return session.exec(select(Tag).offset(offset).limit(limit)).all()

@app.get("/tags/{id}")
async def get_tag_by_id(tag_id: int, session: SessionDep) -> Tag:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found.")
    return tag

@app.post("/tags")
async def create_tag(tag: Annotated[TagCreate, Form()], session: SessionDep) -> Tag:
    db_tag = Tag.model_validate(tag)
    session.add(tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag