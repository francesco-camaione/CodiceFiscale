from data import dictionaries
from database import mysql_dtb
from main.util import utils
from main.service import codici_catastali_service

# richiesta user input

# cognome = ''
# nome = input("Qual'è il tuo nome? ")
# sesso = input('Sesso?(M - F): ')
# data_dn = input('Inserisci la tua  data di nascita in DD MM YYYY: ')
# comune_input = input('Inserisci il comune di nascita: ')
# provincia_input = input('Inserisci la provincia di nascita: ')


# calcolo ultime due cifre dell'anno, lettera mese, cifra giorno di nascita in base al sesso
def funzione_data(data_dn, sesso):
    day, month, year = map(int, data_dn.split(' '))
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
        day_cf = day + 40

    day_cf_str = str(day_cf)  # giorno
    data_di_n = str(year_codicefiscale + letter_month + day_cf_str)
    return data_di_n


# calcolo codice catastale (4 caratteri)
def funzione_cod_catastale(comune, provincia):
    indice_comune = ''
    indice_provincia = ''
    comune_input_2 = comune.upper()[0] + comune[1:]
    provincia_input_2 = provincia.upper()[0] + provincia[1:]
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
    return codice_catastale


# carattere di controllo (1 lettera)
def funz_car_controllo(cognome, nome, data, codice_cat):
    codice_fiscale = str(utils.Utils.funzione_cognomi(cognome)) + str(utils.Utils.funzione_nomi(nome)) \
                     + str(data) + str(codice_cat)
    dispari1 = (codice_fiscale[14] + codice_fiscale[12] + codice_fiscale[10] + codice_fiscale[8] + codice_fiscale[6]
                + codice_fiscale[4] + codice_fiscale[2] + codice_fiscale[0]).upper()

    pari2 = (codice_fiscale[13] + codice_fiscale[11] + codice_fiscale[9]
             + codice_fiscale[7] + codice_fiscale[5] + codice_fiscale[3] + codice_fiscale[1]).upper()

    valori_disp = (dictionaries.dispari[dispari1[0]] + dictionaries.dispari[dispari1[1]] + dictionaries.dispari[dispari1[2]]
                   + dictionaries.dispari[dispari1[3]] + dictionaries.dispari[dispari1[4]]
                   + dictionaries.dispari[dispari1[5]] + dictionaries.dispari[dispari1[6]] +
                   dictionaries.dispari[dispari1[7]])

    valori_pari = (dictionaries.pari[pari2[0]] + dictionaries.pari[pari2[1]] + dictionaries.pari[pari2[2]] +
                   dictionaries.pari[pari2[3]] + dictionaries.pari[pari2[4]] + dictionaries.pari[pari2[5]] +
                   dictionaries.pari[pari2[6]])
    tot = (valori_pari + valori_disp)
    tot_div = tot % 26
    carattere_controllo = dictionaries.controllo[tot_div]
    return carattere_controllo


# output codice fiscale
def output(cognome, nome, year_codicefiscale, letter_month, day_cf_str, codice_catastale, carattere_controllo):
    cod = utils.Utils.funzione_cognomi(cognome) + utils.Utils.funzione_nomi(nome) + year_codicefiscale \
      + letter_month + day_cf_str + codice_catastale + carattere_controllo
    codice = cod.upper()
    return codice


# saving user data
# info_to_dtb = Persona.cognome.upper(), Persona.nome.upper(), Persona.sesso.upper(), Persona.data_dn.upper(),\
# Persona.comune_input.upper(), Persona.provincia_input.upper(), output()
# mysql_dtb.Mysql.store_data(cod, info_to_dtb)


def main():
    pass


if __name__ == '__main':
    main()
