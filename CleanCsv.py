import csv

with open('HouseList.csv', newline='', encoding='utf-8') as infile, open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        
        combined_string = ''.join(row)
       
        writer.writerow([combined_string])


