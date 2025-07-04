from typing import List
from sqlmodel import Field, Relationship, SQLModel
from app.models.hero_team import HeroTeamLink

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None