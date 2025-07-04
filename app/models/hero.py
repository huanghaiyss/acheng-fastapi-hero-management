from typing import List
from sqlmodel import Field, Relationship, SQLModel
from app.models.hero_team import HeroTeamLink

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="heroes", link_model=HeroTeamLink)

class HeroCreate(HeroBase):
    team_ids: List[int] = []

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_ids: List[int] | None = None