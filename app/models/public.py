from typing import List
from sqlmodel import SQLModel

class HeroPublic(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None

class TeamPublic(SQLModel):
    id: int
    name: str
    headquarters: str

class HeroPublicWithTeams(HeroPublic):
    teams: List[TeamPublic] = []

class TeamPublicWithHeroes(TeamPublic):
    heroes: List[HeroPublic] = []