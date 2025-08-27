from sqlmodel import Relationship, SQLModel, Field


class RestaurantTagLink(SQLModel, table=True):
    restaurant_id: int | None = Field(default=None, foreign_key="restaurant.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True,)
    name: str = Field(index=True)

    restaurants: list["Restaurant"] = Relationship(back_populates="tags", link_model=RestaurantTagLink)

class Restaurant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True,)
    name: str = Field(index=True)
    description: str | None = Field(default=None, nullable=True)
    price: int | None = Field(default=None, nullable=True)
    address: str | None = Field(default=None, nullable=True)

    tags: list[Tag] = Relationship(back_populates="restaurants", link_model=RestaurantTagLink)