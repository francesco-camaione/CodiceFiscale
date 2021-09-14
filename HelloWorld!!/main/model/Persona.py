from main.script import app


class Persona:

    def __init__(self):
        self.cognome = app.cognome
        self.nome = app.nome
        self.sesso = app.sesso
        self.data_dn = app.data_dn
        self.comune = app.comune_input
        self.provincia = app.provincia_input
