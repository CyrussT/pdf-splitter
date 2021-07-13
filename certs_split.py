import PyPDF2
import csv
import os

names = list()

pdfName = input("Please input merged pdf name: ")
csvName = input("Please enter csv name: ")
folderName = input("Please enter folder name (make sure you have created the folder): ")

with open("./"+ csvName + ".csv") as file:
    reader = csv.reader(file)
    for row in reader:
        names.append(row)

print("Successfully loaded all names")

file = open("./"+ pdfName +".pdf", "rb")

infile = PyPDF2.PdfFileReader(file)
outfile = PyPDF2.PdfFileWriter()

for page in range(infile.getNumPages()):
    print("Generating page: " + str(page+1))
    current = infile.getPage(page)
    outfile = PyPDF2.PdfFileWriter()
    outfile.addPage(current)

    write_dir = "./"+ folderName + "/"+ names[page][1] + "/"
    file_name = names[page][0] +".pdf"

    if not os.path.exists(write_dir):
        os.makedirs(write_dir)

    with open(write_dir + file_name, "wb") as outstream:
        outfile.write(outstream)

file.close()