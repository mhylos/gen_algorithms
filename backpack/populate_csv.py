import csv
from random import randint

with open('items.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(30):
        writer.writerow(["Item " + str(i), str(randint(1, 10)),
                         str(randint(1, 2000))])
