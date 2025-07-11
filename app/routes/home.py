from urllib import request

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.modelsSQL import *
from app.db_operations import *
from app.db_connection import get_session

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
@router.get("/OK", response_class=HTMLResponse)
async def OK(request: Request):
    return templates.TemplateResponse("OK.html", {"request": request})

@router.get("/information", response_class=HTMLResponse)
async def read_info(request: Request):
    return templates.TemplateResponse("infor.html", {"request": request})

@router.get("/addProfile", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("add_profile.html", {"request": request})

@router.post("/addProfile")
async def submit_info(request:Request,
        Name: str = Form(...),
        Relationship: str = Form(...),
        Message: str = Form(...),
        Image_path: str = Form(...),
        Confirmation: bool = Form(...),
        session: AsyncSession = Depends(get_session)
):
    sesion = ProfileSQL(Name=Name, Relationship=Relationship, Message=Message, Image_path=Image_path, Confirmation=Confirmation)
    await create_profile(session, sesion)
    return RedirectResponse(url="/OK", status_code=303)

@router.get("/profile/{id}", response_class=HTMLResponse)
async def detail_profile(request: Request,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    profile = await get_profile_by_id(session, id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return

@router.get("/allProfiles", response_class=HTMLResponse)
async def all_profiles(request: Request, session: AsyncSession = Depends(get_session)):
    profiles = await get_profiles(session)
    if not profiles:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return templates.TemplateResponse("all_profiles.html", {"request": request, "profiles": profiles})