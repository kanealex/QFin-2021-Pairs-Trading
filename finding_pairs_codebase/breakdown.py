import csv
import pandas





# open file in read mode
with open('starting_data.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    newfile = False
    tikerfile = None
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        if(row == []):
            newfile = True
        elif(newfile):
            tickername = "ticker_breakdown/Real_Estate/" + row[0] + ".csv"
            tikerfile = open(tickername, 'w', newline='')
            newfile = False 
        else:
            writer = csv.writer(tikerfile)
            writer.writerow(row)


