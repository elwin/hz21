import csv
import os
import random


default_customers = [
    94290,
    74310,
    44880,
    90471,
    34390,
]

for filename in os.listdir('resources/shopping_cart/'):

    header = []
    data = []
    customer_assignments = {}

    with open('resources/shopping_cart/' + filename) as f_in:
        r = csv.reader(f_in, delimiter=',')
        for i, row in enumerate(r):
            if i==0:
                header = row
                continue

            customer_id = int(row[1])
            if customer_id not in default_customers:
                if customer_id not in customer_assignments:
                    customer_assignments[customer_id] = random.choice(default_customers)
                row[2] = str(row[1]+row[2])
                row[1] = str(customer_assignments[customer_id])
            data.append(row)

    with open('resources/shopping_cart_new/' + filename, 'w', newline='', encoding="utf-8") as f_out:
        w = csv.writer(f_out, delimiter=',', quotechar="'")
        w.writerow(header)
        w.writerows(data)
