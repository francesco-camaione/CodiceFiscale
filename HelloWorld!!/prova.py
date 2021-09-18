import main.script.app
import mysql.connector
import main.service.FiscalCodeCalculatorService
try:

    mydtb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Golftdi11',
        port='3306',
        database='cod_fiscale',
    )

    cursor = mydtb.cursor()
    mySql_insert_query = """INSERT INTO dati_cf (Cognome, Nome, Sesso, Data_di_nascita, Comune, Provincia, Codice_Fisc) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s) """

    record = (main.script.app.cognome.upper(), main.script.app.nome.upper(), main.script.app.sesso.upper(), main.script.app.data_dn.upper(), main.script.app.comune_input.upper(),
              main.script.app.provincia_input.upper(), main.service.FiscalCodeCalculatorService.cod.upper())
    cursor.execute(mySql_insert_query, record)
    mydtb.commit()
    print("Record inserted successfully into Laptop table")

except mysql.connector.Error as error:
    print("Failed to insert into MySQL table {}".format(error))

finally:
    if mydtb.is_connected():
        cursor.close()
        mydtb.close()

