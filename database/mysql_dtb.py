import mysql.connector


class Mysql:

    def store_data(self, record):

        try:

            mydtb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Golftdi11',
                port='3306',
                database='cod_fiscale',
            )

            cursor = mydtb.cursor()
            mysql_insert_query = """
                            INSERT INTO dati_cf (Cognome, Nome, Sesso, Data_di_nascita, Comune, Provincia, Codice_Fisc) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                            """

            record = record
            cursor.execute(mysql_insert_query, record)
            mydtb.commit()
            print("Record inserted successfully into Laptop table")

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

        finally:
            if mydtb.is_connected():
                cursor.close()
                mydtb.close()
            else:
                pass


def main():
    pass


if __name__ == '__main':
    main()
