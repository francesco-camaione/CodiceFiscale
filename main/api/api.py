import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import data.dictionaries
import database.mysql_dtb
import main.service.codici_catastali_service
import main.util.utils

app = FastAPI()

templates = Jinja2Templates(directory="src/build/")
port = int(os.environ.get("PORT", 5000))


@app.get("/")
def form_post(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/c")
def post_comuni(provincia: str):
    comuni_list_ = main.util.utils.comuni_poss3(provincia)
    return comuni_list_


@app.post("/")
def input_user(request: Request, nome: str = Form(...), cognome: str = Form(...), sesso: str = Form(...),
               giorno=Form(...), mese=Form(...), anno=Form(...), provincia: str = Form(...), comune: str = Form(...)):
    day = giorno
    month = mese
    year = anno
    year_str = str(year)
    year_codicefiscale = year_str[2] + year_str[3]  # anno
    letter_month = data.dictionaries.dizionario_mesi[str(month)]  # lettera_mese
    day_cf = 0

    if sesso.lower() == 'm':
        day_cf = day
    if day in range(1, 10):
        str_day = str(day)
        day_cf = str('0' + str_day)
    if sesso.lower() == 'f':
        day_cf = int(day) + 40

    day_cf_str = str(day_cf)  # giorno

    # calcolo codice catastale (4 caratteri)

    comune_input_2 = comune
    provincia_input_2 = provincia[0] + provincia[1:]
    indici_possibili_comune = main.util.utils.list_duplicates_of(main.service.codici_catastali_service.CodiciCatastali.
                                                                 comune, comune_input_2)
    indici_possibili_provincia = main.util.utils.list_duplicates_of(main.service.codici_catastali_service.
                                                                    CodiciCatastali.provincia, provincia_input_2)

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

    codice_catastale = main.service.codici_catastali_service.CodiciCatastali.codici_catastale[indice]

    # carattere di controllo (1 lettera)
    codice_fiscale = main.util.utils.funzione_cognomi(cognome) + main.util.utils.funzione_nomi(nome) + \
                     year_codicefiscale + letter_month + day_cf_str + codice_catastale

    dispari1 = (codice_fiscale[14] + codice_fiscale[12] + codice_fiscale[10] + codice_fiscale[8] + codice_fiscale[6] +
                codice_fiscale[4] + codice_fiscale[2] + codice_fiscale[0]).upper()

    pari2 = (codice_fiscale[13] + codice_fiscale[11] + codice_fiscale[9] + codice_fiscale[7] + codice_fiscale[5] +
             codice_fiscale[3] + codice_fiscale[1]).upper()

    valori_disp = (data.dictionaries.dispari[dispari1[0]] + data.dictionaries.dispari[dispari1[1]] +
                   data.dictionaries.dispari[dispari1[2]] + data.dictionaries.dispari[dispari1[3]] +
                   data.dictionaries.dispari[dispari1[4]] + data.dictionaries.dispari[dispari1[5]] +
                   data.dictionaries.dispari[dispari1[6]] + data.dictionaries.dispari[dispari1[7]])

    valori_pari = (data.dictionaries.pari[pari2[0]] + data.dictionaries.pari[pari2[1]] + data.dictionaries.pari[pari2[2]] +
                   data.dictionaries.pari[pari2[3]] + data.dictionaries.pari[pari2[4]] + data.dictionaries.pari[pari2[5]] +
                   data.dictionaries.pari[pari2[6]])

    tot = (valori_pari + valori_disp)
    tot_div = tot % 26
    carattere_controllo = data.dictionaries.controllo[tot_div]

    # output codice fiscale
    cod = main.util.utils.funzione_cognomi(cognome) + main.util.utils.funzione_nomi(nome) + year_codicefiscale + \
        letter_month + day_cf_str + codice_catastale + carattere_controllo
    codice = f'{cod.upper()}'
    # saving user data
    info_to_dtb = cognome.upper(), nome.upper(), sesso.upper(), giorno.upper(), mese.upper(), anno.upper(), \
                  comune.upper(), provincia.upper(), codice
    database.mysql_dtb.Mysql.store_data(cod, info_to_dtb)

    # saving user data
    info_to_dtb = cognome.upper(), nome.upper(), sesso.upper(), year.upper(), comune.upper(), provincia.upper(), \
                  cod.upper()
    database.mysql_dtb.Mysql.store_data(cod, info_to_dtb)

    return templates.TemplateResponse('index.html', context={'request': request, 'codice': codice})
