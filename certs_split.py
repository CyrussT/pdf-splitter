import PyPDF2
import csv
import os
import time
import logging

from PyPDF2.utils import PdfReadError, PyPdfError

# array to store the names and companies
names = list()
# array to filter out characters to remove
unwanted_chars = ["/", "\t", ":", "!", ";"]

#setting up of logs
clogs = logging.getLogger(__name__)
clogs.setLevel(logging.DEBUG)

# handler 1 - writer
file = logging.FileHandler("certs.log")
file.setLevel(logging.DEBUG)
fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s",datefmt="%H:%M:%S")
file.setFormatter(fileformat)

# handler 2 - to stream
stream = logging.StreamHandler()
streamformat = logging.Formatter("%(levelname)s:%(module)s:%(message)s")
stream.setFormatter(streamformat)

clogs.addHandler(file)
clogs.addHandler(stream)
# end of logging 

# request for file name & check if valid if not raise errors
pdfName = input("Please input Merged PDF file name (excluding the extension .pdf): ")
if not os.path.exists(pdfName+".pdf"):
    clogs.critical("Unable to find file " + pdfName + ".pdf!")
    raise FileNotFoundError
csvName = input("Please enter csv name (excluding the extension .csv): ")
if not os.path.exists(csvName+".csv"):
    clogs.critical("Unable to find file " + csvName + ".csv!")
    raise FileNotFoundError
folderName = input("Please enter folder name (make sure you have created the folder): ")
if not os.path.isdir("./" + folderName + "/"):
    clogs.critical("Unable to find folder: " + folderName)
    raise NotADirectoryError

# open csv file and add to list
with open("./"+ csvName + ".csv") as file:
    reader = csv.reader(file)
    for row in reader:
        #To get rid of the unwanted characters from unwanted_chars list
        for char in unwanted_chars:
            row[0] = row[0].replace(char, "").strip()
            row[1] = row[1].replace(char, "").strip()
        names.append(row)

clogs.info("Successfully loaded " + str(len(names)) + " names!")

# open pdf file
try:
    file = open("./"+ pdfName +".pdf", "rb")
except PyPdfError as e:
    clogs.critical("PyPDF Error: " + e)
    raise PyPdfError

infile = PyPDF2.PdfFileReader(file)
outfile = PyPDF2.PdfFileWriter()

# for each page in the merge file, retrieve the page at x position and save it as a new file
# named as names[0] and directory name under the company as names[1]

for page in range(infile.getNumPages()):
    clogs.info("Generating page: " + str(page+1) + ", for " + names[page][0])
    current = infile.getPage(page)
    outfile = PyPDF2.PdfFileWriter()
    outfile.addPage(current)

    write_dir = "./"+ folderName + "/"+ names[page][1] + "/"
    file_name = names[page][0] +".pdf"

    if not os.path.exists(write_dir):
        try:
            os.makedirs(write_dir)
        except OSError as e:
            clogs.critical("Error: " + e)
            raise
    # write to outfile
    with open(write_dir + file_name, "wb") as outstream:
        outfile.write(outstream)

file.close()
clogs.info("Succesfully generated " + str(len(names)) + " certificates!")
x = input("Press enter to close the program! ")
