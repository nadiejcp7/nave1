# %%
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import random

import nest_asyncio

import uvicorn

from bs4 import BeautifulSoup

# %%
def editHTML(contenido):
    with open("./template/repair_bay.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    div = soup.find("div", class_="anchor-point")
    if div:
        div.string = contenido
        
    with open("./template/repair_bay.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

# %%
sistemas = ["life_support", "engines", "communications", "deflector_shield", "navigation" ]
codes = ["LIFE-03", "ENG-04", "COM-02", "SHLD-05",  "NAV-01"]

pos = random.randint(0, 4)

print("damaged system:", sistemas[pos])
print("damaged code:", codes[pos])

editHTML(codes[pos])

# %%
nest_asyncio.apply()

# %%
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


link = "192.168.100.11"
puerto = 8000
uvicorn.run(app, host=link, port=puerto)




