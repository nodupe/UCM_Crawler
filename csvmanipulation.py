import csv

f = open("ip-10.159.188.100--Al-Khobar.csv",'r')
csv_f = csv.reader(f)

lista = list(csv_f)
i = 0
header = []
while i < (len(lista) - 1):
    header.append(lista[i][0])
    i = i + 1