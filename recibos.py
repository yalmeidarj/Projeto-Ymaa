import PyPDF2
from sqlalchemy import TEXT

def PDFrotate(origFileName, newFileName):
 
    # creating a pdf File object of original pdf
    pdfFileObj = open(origFileName, 'rb')
     
    # creating a pdf Reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
    # creating a pdf writer object for new pdf
    pdfWriter = PyPDF2.PdfFileWriter()
     
    # # rotating each page
    # for page in range(pdfReader.numPages):
 
    #     # creating rotated page object
    #     pageObj = pdfReader.getPage(page)
    #     pageObj.rotateClockwise(rotation)
 
    #     # adding rotated page object to pdf writer
    #     pdfWriter.addPage(pageObj)
 
    # new pdf file object
    newFile = open(newFileName, 'wb')
     
    # writing rotated pages to new file

    # for line in pdfReader:
    # #read replace the string and write to output file
    #     print(line)
    pdfWriter.write(newFile.replace('service_ID', '10'))
 
    # closing the original pdf file object
    pdfFileObj.close()
     
    # closing the new pdf file object
    newFile.close()

PDFrotate('Ymaa-recibo.pdf', 'newFileName.pdf')