from main.model.Persona import Persona
from main.util import utils
from main.script import app


a = Persona()
cod = utils.funzione_cognomi(a.cognome) + utils.funzione_nomi(a.nome) + app.year_codicefiscale + \
      app.letter_month + app.day_cf_str + app.codice_catastale + app.carattere_controllo
