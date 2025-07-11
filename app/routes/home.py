from urllib import request
from pydub import AudioSegment
from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.modelsSQL import *
from app.db_operations import *
from app.db_connection import get_session
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uuid

UPLOAD_DIR ="static/audio"
templates = Jinja2Templates(directory="templates")
router = APIRouter()
###This is the Home Page
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
###This is the response of OK task
@router.get("/OK", response_class=HTMLResponse)
async def OK(request: Request):
    return templates.TemplateResponse("OK.html", {"request": request})
###This is Information Page, like "About Us" pages
@router.get("/information", response_class=HTMLResponse)
async def read_info(request: Request):
    return templates.TemplateResponse("infor.html", {"request": request})
###This is add profile page
@router.get("/addProfile", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("add_profile.html", {"request": request})
###This is the form to add profile page
@router.post("/addProfile")
async def submit_info(
    request: Request,
    Name: str = Form(...),
    Relationship: str = Form(...),
    Message: str = Form(...),
    Image_path: str = Form(...),
    Confirmation: bool = Form(...),
    audio_file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    # 1. Guardar el archivo de audio en static/audio/
    file_ext = audio_file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    save_path = os.path.join("static", "audio", unique_filename)

    with open(save_path, "wb") as buffer:
        buffer.write(await audio_file.read())

    # 2. Guardar la ruta relativa
    audio_relative_path = f"static/audio/{unique_filename}"

    # 3. Crear perfil
    profile = ProfileSQL(
        Name=Name,
        Relationship=Relationship,
        Message=Message,
        Image_path=Image_path,
        Confirmation=Confirmation,
        Audio_path=audio_relative_path
    )

    await create_profile(session, profile)
    return RedirectResponse(url="/OK", status_code=303)
###This is the search by id Page
@router.get("/profile/{id}", response_class=HTMLResponse)
async def detail_profile(request: Request,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    profile = await get_profile_by_id(session, id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return templates.TemplateResponse("profile.html", {"request": request, "profile": profile})
###This show all profiles
@router.get("/allProfiles", response_class=HTMLResponse)
async def all_profiles(request: Request, session: AsyncSession = Depends(get_session)):
    profiles = await get_profiles(session)
    if not profiles:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return templates.TemplateResponse("all_profiles.html", {"request": request, "profiles": profiles})

@router.get("/plot_audio/{id}")
async def plot_audio(id: int, session: AsyncSession = Depends(get_session)):
    profile = await get_profile_by_id(session, id)
    if not profile or not profile.Audio_path:
        raise HTTPException(status_code=404, detail="Audio no encontrado")

    audio = AudioSegment.from_file(profile.Audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Graficar con pandas
    df = pd.DataFrame(samples, columns=["Amplitud"])
    df["Tiempo"] = df.index / audio.frame_rate

    fig, ax = plt.subplots(figsize=(10, 4))
    df.plot(x="Tiempo", y="Amplitud", ax=ax, legend=False)
    ax.set_title("Forma de onda del audio")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")

    plot_path = f"static/plots/audio_plot_{id}.png"
    fig.savefig(plot_path)
    plt.close(fig)

    return FileResponse(plot_path, media_type="image/png")


