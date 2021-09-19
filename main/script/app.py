import database.mysql
from data import dictionaries
from database import mysql
from main.util import utils
from main.service import codici_catastali_service
from main.model.Persona import Persona
# questo va in script
cognome = input("Qual è il tuo cognome? ")
nome = input("Qual'è il tuo nome? ")
sesso = input('Sesso?(M - F): ')
data_dn = input('Inserisci la tua  data di nascita in DD MM YYYY: ')
comune_input = input('Inserisci il comune di nascita: ')
provincia_input = input('Inserisci la provincia di nascita: ')

persona_x = Persona(cognome, nome, sesso, data_dn, comune_input, provincia_input)

# studio le classi e gli oggetti e che vuol dire instanziare una classe

# istanzio la classe Persona
# chiamo il servizio che calcola il codice fiscale

# sposto i metodi "stupidi" nella classe util, ossia quei metodi che non hanno
# stato e che performano un'operazione semplice

day, month, year = map(int, data_dn.split(' '))
year_str = str(year)
year_codicefiscale = year_str[2] + year_str[3]
letter_month = dictionaries.dizionario_mesi[str(month)]
day_cf = 0
str_day = ''

if sesso.lower() == 'm':
    day_cf = day
if day in range(1, 10):
    str_day = str(day)
    day_cf = str('0' + str_day)
if sesso.lower() == 'f':
    day_cf = day + 40

day_cf_str = str(day_cf)

# questa parte e' da inserire in un service apposito.

indice_comune = ''
indice_provincia = ''
comune_input_2 = comune_input.upper()[0] + comune_input[1:]
provincia_input_2 = provincia_input.upper()[0] + provincia_input[1:]
indici_possibili_comune = utils.list_duplicates_of(codici_catastali_service.CodiciCatastali.comune, comune_input_2)
indici_possibili_provincia = utils.list_duplicates_of(codici_catastali_service.CodiciCatastali.provincia, provincia_input_2)

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
codice_fiscale = utils.funzione_cognomi(cognome) + utils.funzione_nomi(nome) + year_codicefiscale + letter_month +\
                 day_cf_str + codice_catastale
dispari1 = codice_fiscale[14].upper() + codice_fiscale[12].upper() + codice_fiscale[10].upper() + \
           codice_fiscale[8].upper() + codice_fiscale[6].upper() + codice_fiscale[4].upper() + \
           codice_fiscale[2].upper() + codice_fiscale[0].upper()
pari2 = codice_fiscale[13].upper() + codice_fiscale[11].upper() + codice_fiscale[9].upper() +\
        codice_fiscale[7].upper() + codice_fiscale[5].upper() + codice_fiscale[3].upper() + codice_fiscale[1].upper()
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
# questo e' il file che va eseguito, mi aspetto quindi che scriva in output il codice fiscale
cod = utils.funzione_cognomi(cognome) + utils.funzione_nomi(nome) + year_codicefiscale + \
      letter_month + day_cf_str + codice_catastale + carattere_controllo

print(f"il tuo codice fiscale è: {cod.upper()}")

info_to_dtb = cognome.upper(), nome.upper(), sesso.upper(), data_dn.upper(), comune_input.upper(), provincia_input.upper(), cod.upper()
mysql.Mysql.store_data(cod, info_to_dtb)
