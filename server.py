from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

import random
import os

import uvicorn
from bs4 import BeautifulSoup

def getFunctionValues(p1, p2):
    #y = mx +b
    m = (p2[1]-p1[1])/(p2[0]-p1[0])
    b = p2[1]-p2[0]*m
    return m, b

def editHTML(contenido):
    with open("./template/repair_bay.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    div = soup.find("div", class_="anchor-point")
    if div:
        div.string = contenido
        
    with open("./template/repair_bay.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

sistemas = ["life_support", "engines", "communications", "deflector_shield", "navigation" ]
codes = ["LIFE-03", "ENG-04", "COM-02", "SHLD-05",  "NAV-01"]
pos = random.randint(0, 4)
editHTML(codes[pos])

p1 = [0.00105, 0.05]
p2 = [0.0035, 10]
p3 = [30, 0.05]

ml, bl = getFunctionValues(p1, p2)
mv, bv = getFunctionValues(p3, p2)

app = FastAPI()
templates = Jinja2Templates(directory="template")

@app.get("/status", response_class=JSONResponse, tags=["API"])
def get_status():
    print('entered status')
    return {"damaged_system": sistemas[pos]}

@app.get("/repair-bay", response_class=HTMLResponse, tags=["HTML"])
def get_repair_bay(request: Request):
    print('entered repair-bay')
    return templates.TemplateResponse("repair_bay.html", {"request": request})

@app.post("/teapot", tags=["Fun"])
def teapot():
    print('entered teapot')
    return Response(content="I'm a teapot", status_code=status.HTTP_418_IM_A_TEAPOT)

@app.get("/phase-change-diagram")
def get_phase_change_diagram(pressure: float):
    svl = (pressure - bl)/ml
    svv = (pressure - bv)/mv
    return {
                "specific_volume_liquid": svl,
                "specific_volume_vapor": svv
            }


link = "0.0.0.0"
puerto = int(os.environ.get("PORT", 8000))  
uvicorn.run(app, host=link, port=puerto)




