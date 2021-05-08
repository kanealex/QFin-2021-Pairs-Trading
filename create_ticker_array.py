import csv
import pandas


# open file in read mode
with open('SectorTickers/Real_Estate.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    tickerarray = []
    for row in csv_reader:
        tickerarray.append(row[0])
    print(tickerarray)