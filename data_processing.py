import csv

# open input CSV file as source
# open output CSV file as result
with open("student/student-mat.csv", "r") as source:
    reader = csv.reader(source, delimiter = ';')
    
    with open("output.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
            # we only processing the int type data
            writer.writerow((r[2], r[6], r[7], r[12], r[13], r[14], r[23], r[24], r[25], r[26], r[27], r[28], r[29], r[30], r[31], r[32]))