

from fastapi import FastAPI, Depends
from db_connection import get_session, init_db
from db_operations import *
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup():
    await init_db()
###Crear usuario
@app.post("/profile", tags=["Profiles"])
async def create_profile(profile: ProfileSQL, session: AsyncSession = Depends(get_session)):
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


###Mostrar todos los usuarios
@app.get("/profiles/", response_model=List[ProfileSQL], tags=["Profiles"])
async def all_profiles(session: AsyncSession = Depends(get_session)):
    results = await session.execute(select(ProfileSQL))
    profiles= results.scalars().all()
    return profiles
###Mostrar los usuarios filtrados porID
@app.get("/profiles/{profile_id}", response_model=ProfileSQL, tags=["Profiles"])
async def get_profile_by_id(profile_id: int, session: AsyncSession = Depends(get_session)):
    profile = await session.get(ProfileSQL, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no registrado")
    return profile
##Actualizar usuarios
@app.put("/profiles/{profile_id}", response_model=ProfileSQL)
async def update_profile_by_id(profile_id: int, update_data: ProfileUpdate, session: AsyncSession = Depends(get_session)):
    updated = await update_profile(session, profile_id, update_data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated
