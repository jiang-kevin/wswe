from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import Database
from models import Restaurant, Tag

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


@app.get("/restaurants")
async def get_restaurants(session: SessionDep) -> list[Restaurant]:
    restaurants = list(session.exec(select(Restaurant)).all())
    return restaurants

@app.get("/restaurants/{id}")
async def get_restaurant_by_id(restaurant_id: int, session: SessionDep):
    return session.get(Restaurant, restaurant_id)

@app.post("/restaurants")
async def create_restaurant(restaurant: Annotated[Restaurant, Form()], session: SessionDep):
    session.add(restaurant)
    session.commit()

@app.get("/tags")
async def get_tags(session: SessionDep):
    return session.exec(select(Tag)).all()

@app.get("/tags/{id}")
async def get_tag_by_id(tag_id: int, session: SessionDep):
    return session.get(Tag, tag_id)

@app.post("/tags")
async def create_tag(tag: Annotated[Tag, Form()], session: SessionDep):
    session.add(tag)
    session.commit()