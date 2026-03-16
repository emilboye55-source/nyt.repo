import csv
from datetime import datetime
import time

tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Program startede kl: {tid}")
    # opretter txt fil og skriver tidspunkt for hver iteration i den
    
with open('Dato.txt', 'a', encoding='utf-8') as file:
        file.write(f"Program kørte kl: {tid}\n")
   
with open('Dato.csv', 'a', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow([tid])