import csv

csv_f = csv.reader(open('file_to_date.csv','r'), delimiter=',')
all_ids = set()

for row in csv_f:
    if row[0] in all_ids:
        print(row[0])
    all_ids.add(row[0])

print(len(all_ids))