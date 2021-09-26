from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from main.script import appl
from main.util.utils import Utils

app = FastAPI()
templates = Jinja2Templates(directory="src/build/")
output = ''


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get("/form")
def form_post(request: Request):
    result = "Type"
    return templates.TemplateResponse('form1.html', context={'request': request, 'result': result})


@app.post("/form")
def input_user(request: Request, nome: str = Form(...), cognome: str = Form(...), sesso: str = Form(...),
               data_dn=Form(...), comune: str = Form(...), provincia: str = Form(...)):
    data_di_nas = appl.funzione_data(data_dn, sesso)
    codice_catast = appl.funzione_cod_catastale(comune, provincia)
    output = Utils.funzione_cognomi(cognome) + Utils.funzione_nomi(nome) + appl.funzione_data(data_dn, sesso) \
        + appl.funzione_cod_catastale(comune, provincia) + \
        appl.funz_car_controllo(cognome, nome, data_di_nas, codice_catast)
    return templates.TemplateResponse('form1.html', context={'request': request, 'result': output})

