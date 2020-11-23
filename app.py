import ee

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src import ee_map
from src import utils

# Init Earth Engine
utils.load_credentials()
ee.Initialize()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "year":2020})

@app.get("/methodology")
async def methodology(request: Request):
    return templates.TemplateResponse("methodology.html", {"request": request, "year":2020})

@app.get("/map")
async def map(request: Request):
    ee_map.position(-77.08767, -11.97586, 18) 
    ee_map.restart()
    return templates.TemplateResponse("map.html", {"request": request})

@app.post('/map')
async def form_post(request: Request):
    ee_map.position(0,0,2)
    ee_map.addTile(geoviz=None)
    return templates.TemplateResponse('map.html', {'request': request})

@app.post("/map/geometria")
async def geometria(request: Request):
    geometries = await request.body()
    print(geometries)
