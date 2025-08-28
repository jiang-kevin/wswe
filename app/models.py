from sqlmodel import Relationship, SQLModel, Field


class RestaurantTagLink(SQLModel, table=True):
    restaurant_id: int | None = Field(default=None, foreign_key="restaurant.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class RestaurantBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None, nullable=True)
    price: int | None = Field(default=None, nullable=True)
    address: str | None = Field(default=None, nullable=True)

class Restaurant(RestaurantBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tags: list["Tag"] = Relationship(back_populates="restaurants", link_model=RestaurantTagLink)

class RestaurantCreate(RestaurantBase):
    tag_ids: list[int]

class RestaurantPublic(RestaurantBase):
    id: int

class TagBase(SQLModel):
    name: str = Field(index=True)

class Tag(TagBase, table=True):
    id: int | None = Field(default=None, primary_key=True,)
    restaurants: list[Restaurant] = Relationship(back_populates="tags", link_model=RestaurantTagLink)

class TagCreate(TagBase):
    pass

class TagPublic(TagBase):
    id: int

class RestaurantPublicWithTags(RestaurantPublic):
    tags: list[TagPublic] = []