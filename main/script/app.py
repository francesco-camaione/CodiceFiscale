from data import dictionaries
from database import mysql_dtb
from main.util import utils
from main.service import codici_catastali_service
from main.model.Persona import Persona

# richiesta user input
cognome = input("Qual è il tuo cognome? ")
nome = input("Qual'è il tuo nome? ")
sesso = input('Sesso?(M - F): ')
data_dn = input('Inserisci la tua  data di nascita in DD MM YYYY: ')
comune_input = input('Inserisci il comune di nascita: ')
provincia_input = input('Inserisci la provincia di nascita: ')

persona_x = Persona(cognome, nome, sesso, data_dn, comune_input, provincia_input)

# calcolo ultime due cifre dell'anno, lettera mese, cifra giorno di nascita in base al sesso

day, month, year = map(int, persona_x.data_dn.split(' '))
year_str = str(year)
year_codicefiscale = year_str[2] + year_str[3]
letter_month = dictionaries.dizionario_mesi[str(month)]
day_cf = 0
str_day = ''

if persona_x.sesso.lower() == 'm':
    day_cf = day
if day in range(1, 10):
    str_day = str(day)
    day_cf = str('0' + str_day)
if persona_x.sesso.lower() == 'f':
    day_cf = day + 40

day_cf_str = str(day_cf)

# calcolo codice catastale (4 caratteri)
indice_comune = ''
indice_provincia = ''
comune_input_2 = persona_x.comune_input.upper()[0] + persona_x.comune_input[1:]
provincia_input_2 = persona_x.provincia_input.upper()[0] + persona_x.provincia_input[1:]
indici_possibili_comune = utils.Utils.list_duplicates_of(codici_catastali_service.CodiciCatastali.comune, comune_input_2)
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
codice_fiscale = utils.Utils.funzione_cognomi(persona_x.cognome) + utils.Utils.funzione_nomi(persona_x.nome) \
                 + year_codicefiscale + letter_month + day_cf_str + codice_catastale

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

# output codice fiscale
cod = utils.Utils.funzione_cognomi(persona_x.cognome) + utils.Utils.funzione_nomi(persona_x.nome) + year_codicefiscale \
      + letter_month + day_cf_str + codice_catastale + carattere_controllo
codice = cod.upper()
print(f"il tuo codice fiscale è: {codice}")

# saving user data
info_to_dtb = persona_x.cognome.upper(), persona_x.nome.upper(), persona_x.sesso.upper(), persona_x.data_dn.upper(),\
              persona_x.comune_input.upper(), persona_x.provincia_input.upper(), codice
mysql_dtb.Mysql.store_data(cod, info_to_dtb)


def main():
    pass


if __name__ == '__main':
    main()
