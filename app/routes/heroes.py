from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.hero import Hero, HeroCreate, HeroUpdate
from app.models.team import Team
from app.models.public import HeroPublicWithTeams
from app.auth import get_current_user
router = APIRouter()

@router.post("/", response_model=HeroPublicWithTeams)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    if hero.team_ids:
        teams = session.exec(select(Team).where(Team.id.in_(hero.team_ids))).all()
        if len(teams) != len(hero.team_ids):
            raise HTTPException(status_code=404, detail="One or more teams not found")
        db_hero.teams = teams
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=List[HeroPublicWithTeams])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@router.get("/{hero_id}", response_model=HeroPublicWithTeams)
def read_hero(*, session: Session = Depends(get_session),hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.patch("/{hero_id}", response_model=HeroPublicWithTeams)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate,current_hero: dict = Depends(get_current_user)
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        if key == "team_ids":
            teams = session.exec(select(Team).where(Team.id.in_(value))).all()
            if len(teams) != len(value):
                raise HTTPException(status_code=404, detail="One or more teams not found")
            db_hero.teams = teams
        else:
            setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.delete("/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int,current_hero: dict = Depends(get_current_user)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

@router.post("/{hero_id}/teams/{team_id}", response_model=HeroPublicWithTeams)
def add_hero_to_team(
    *, session: Session = Depends(get_session), hero_id: int, team_id: int
):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)
    if not hero or not team:
        raise HTTPException(status_code=404, detail="Hero or team not found")
    if team not in hero.teams:
        hero.teams.append(team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
    return hero

@router.delete("/{hero_id}/teams/{team_id}", response_model=HeroPublicWithTeams)
def remove_hero_from_team(
    *, session: Session = Depends(get_session), hero_id: int, team_id: int
,current_hero: dict = Depends(get_current_user)):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)
    if not hero or not team:
        raise HTTPException(status_code=404, detail="Hero or team not found")
    if team in hero.teams:
        hero.teams.remove(team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
    return hero
