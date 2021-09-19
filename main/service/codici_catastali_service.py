import csv
# questa parte e' da inserire in un service apposito.


class CodiciCatastali:
    comune, regione, provincia, codici_catastale = [], [], [], []
    with open('C:/Users/franc/PycharmProjects/pythonProject/HelloWorld!!/data/codici.csv', 'r') as file_in:
        reader = csv.reader(file_in, delimiter=',')
        for row in reader:
            comune.append(row[1])
            regione.append(row[2])
            provincia.append(row[3])
            codici_catastale.append(row[4])

