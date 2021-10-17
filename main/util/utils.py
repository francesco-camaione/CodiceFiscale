from fastapi.encoders import jsonable_encoder
from main.service import codici_catastali_service


def funzione_cognomi(cognome: str):
    i = 0
    cognome_ = cognome.strip()
    treconsonanti = ''
    vocali = 'a' 'e' 'i' 'o' 'u' ' ' 'A' 'E' 'I' 'O' 'U'
    vocali_cognome = ''
    hotrovatotreoccorenze = True
    consonanti_cognome = ''
    while i < len(cognome_) and hotrovatotreoccorenze:
        if cognome_[i] in vocali:
            vocali_cognome += cognome_[i]
        if cognome_[i] not in vocali:
            consonanti_cognome += cognome_[i]
        if len(consonanti_cognome) == 3:
            treconsonanti = consonanti_cognome[0] + consonanti_cognome[1] + consonanti_cognome[2]
        if len(consonanti_cognome) == 2:
            treconsonanti = consonanti_cognome[0] + consonanti_cognome[1] + vocali_cognome[0]
        if len(consonanti_cognome) == 1 and len(vocali_cognome) == 1:
            treconsonanti = consonanti_cognome[0] + vocali_cognome[0] + 'X'

        i += 1
    return treconsonanti


def funzione_nomi(nome: str):
    cf_nome = 0
    correct_v_n = ''
    consonanti_nome = ''
    vocali_nome = ''
    condizione = True
    vocali = 'a' 'e' 'i' 'o' 'u' ' ' 'A' 'E' 'I' 'O' 'U'
    while cf_nome < len(nome) and condizione:
        if nome[cf_nome] not in vocali:
            consonanti_nome += nome[cf_nome]
        if nome[cf_nome] in vocali:
            vocali_nome += nome[cf_nome]
        if len(consonanti_nome) == 4:
            correct_v_n = consonanti_nome[0:1] + consonanti_nome[2:3] + consonanti_nome[3:4]
        if len(consonanti_nome) == 3:
            correct_v_n = consonanti_nome[0:1] + consonanti_nome[1:2] + consonanti_nome[2:3]
        if len(consonanti_nome) == 2:
            correct_v_n = consonanti_nome[0:1] + consonanti_nome[1:2] + vocali_nome[0:1]

        cf_nome += 1
    return correct_v_n


def list_duplicates_of(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def comuni_poss3(provincia: str):
    provincia_input_2 = provincia[0] + provincia[1:]
    indici_possibili_provincia = list_duplicates_of(codici_catastali_service.CodiciCatastali.provincia,
                                                    provincia_input_2)
    z = 0
    condiz = True
    comuni_list2 = ''
    while condiz:
        try:
            c = indici_possibili_provincia[z]
            z += 1
            comuni_poss = codici_catastali_service.CodiciCatastali.comune[c]
            comuni_list2 += f"<option>{comuni_poss}</option>"
        except IndexError:
            condiz = False
    comuni_list = jsonable_encoder(comuni_list2)
    return comuni_list
