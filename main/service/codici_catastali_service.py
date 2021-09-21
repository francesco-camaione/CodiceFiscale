import csv


class CodiciCatastali:
    comune, regione, provincia, codici_catastale = [], [], [], []
    with open('C:/Users/franc/CodiceFiscale/data/codici.csv', 'r') as file_in:
        reader = csv.reader(file_in, delimiter=',')
        for row in reader:
            comune.append(row[1])
            regione.append(row[2])
            provincia.append(row[3])
            codici_catastale.append(row[4])


def main():
    pass


if __name__ == '__main':
    main()
