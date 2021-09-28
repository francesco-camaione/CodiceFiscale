from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from data import dictionaries
from database import mysql_dtb
from main.service import codici_catastali_service
from main.util import utils
import os

app = FastAPI()
templates = Jinja2Templates(directory="src/build/")

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)


@app.get("/")
def form_post(request: Request):
    result = "Type"
    return templates.TemplateResponse('index.html', context={'request': request, 'result': result})


@app.post("/")
def input_user(request: Request, nome: str = Form(...), cognome: str = Form(...), sesso: str = Form(...),
               giorno=Form(...), mese=Form(...), anno=Form(...), comune: str = Form(...), provincia: str = Form(...)):
    day = giorno
    month = mese
    year = anno
    year_str = str(year)
    year_codicefiscale = year_str[2] + year_str[3]  # anno
    letter_month = dictionaries.dizionario_mesi[str(month)]  # lettera_mese
    day_cf = 0
    str_day = ''

    if sesso.lower() == 'm':
        day_cf = day
    if day in range(1, 10):
        str_day = str(day)
        day_cf = str('0' + str_day)
    if sesso.lower() == 'f':
        day_cf = int(day) + 40

    day_cf_str = str(day_cf)  # giorno

    # calcolo codice catastale (4 caratteri)
    indice_comune = ''
    indice_provincia = ''
    comune_input_2 = comune.upper()[0] + comune[1:]
    provincia_input_2 = provincia.upper()[0] + provincia.lower()[1:]
    indici_possibili_comune = utils.Utils.list_duplicates_of(codici_catastali_service.CodiciCatastali.comune,
                                                             comune_input_2)
    indici_possibili_provincia = utils.Utils.list_duplicates_of(codici_catastali_service.CodiciCatastali.provincia,
                                                                provincia_input_2)

    condiz = True
    g = 0
    indice = ''
    while condiz:
        if indici_possibili_comune[g] not in indici_possibili_provincia:
            pass
        else:
            indice = indici_possibili_comune[g]
            condiz = False
        g += 1

    codice_catastale = codici_catastali_service.CodiciCatastali.codici_catastale[indice]

    # carattere di controllo (1 lettera)
    codice_fiscale = utils.Utils.funzione_cognomi(cognome) + utils.Utils.funzione_nomi(nome) + year_codicefiscale \
                     + letter_month + day_cf_str + codice_catastale

    dispari1 = (codice_fiscale[14] + codice_fiscale[12] + codice_fiscale[10] + codice_fiscale[8] + codice_fiscale[6] +
                codice_fiscale[4] + codice_fiscale[2] + codice_fiscale[0]).upper()

    pari2 = (codice_fiscale[13] + codice_fiscale[11] + codice_fiscale[9] + codice_fiscale[7] + codice_fiscale[5] +
             codice_fiscale[3] + codice_fiscale[1]).upper()

    valori_disp = (dictionaries.dispari[dispari1[0]] + dictionaries.dispari[dispari1[1]] +
                   dictionaries.dispari[dispari1[2]] + dictionaries.dispari[dispari1[3]] +
                   dictionaries.dispari[dispari1[4]] + dictionaries.dispari[dispari1[5]] +
                   dictionaries.dispari[dispari1[6]] + dictionaries.dispari[dispari1[7]])

    valori_pari = (dictionaries.pari[pari2[0]] + dictionaries.pari[pari2[1]] + dictionaries.pari[pari2[2]] +
                   dictionaries.pari[pari2[3]] + dictionaries.pari[pari2[4]] + dictionaries.pari[pari2[5]] +
                   dictionaries.pari[pari2[6]])

    tot = (valori_pari + valori_disp)
    tot_div = tot % 26
    carattere_controllo = dictionaries.controllo[tot_div]

    # output codice fiscale
    cod = utils.Utils.funzione_cognomi(cognome) + utils.Utils.funzione_nomi(nome) + year_codicefiscale + \
          letter_month + day_cf_str + codice_catastale + carattere_controllo
    codice = f'Il codice fiscale è:  {cod.upper()}'
    # saving user data
    info_to_dtb = cognome.upper(), nome.upper(), sesso.upper(), giorno.upper(), mese.upper(), anno.upper(), \
                  comune.upper(), provincia.upper(), codice
    mysql_dtb.Mysql.store_data(cod, info_to_dtb)

    # saving user data
    info_to_dtb = cognome.upper(), nome.upper(), sesso.upper(), year.upper(), comune.upper(), provincia.upper(), \
                  cod.upper()
    mysql_dtb.Mysql.store_data(cod, info_to_dtb)

    return templates.TemplateResponse('index.html', context={'request': request, 'codice': codice})
