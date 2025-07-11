from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, List, Optional, Dict
from fastapi import HTTPException
from modelsSQL import *
##Crear usuario
async def create_profile(session: Session, profile:ProfileSQL):
    db_profile = ProfileSQL.model_validate(profile, from_attributes=True)
    session.add(db_profile)
    await session.commit()
    await session.refresh(db_profile)
    return db_profile
###Traer todos los usuarios
async def get_profiles(session: Session):
    query = select(ProfileSQL)
    results = await session.exec(query)
    profiles = results.all()
    return profiles
##Traer usuario por id
async def get_profile_by_id(session: Session, profile_id:int):
    return await session.get(ProfileSQL, profile_id)
#modificar usuario

async def update_profile(session: Session, profile_id:int, profile_update:Dict[str, Any]):
     profile = await session.get(ProfileSQL, profile_id)
     if profile is None:
         return None
     for key, value in profile_update.items():
         if hasattr(profile, key) and value is not None:
             setattr(profile, key, value)
     session.add(profile)
     await session.commit()
     await session.refresh(profile)
     return profile