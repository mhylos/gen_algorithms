import csv
from random import randint

with open('coords.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(7):
        writer.writerow([str(randint(1, 100)), str(randint(1, 100))])
