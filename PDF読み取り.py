# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTContainer,
    LTTextLine,
)
import camelot
from io import StringIO
import os
import tabula
import pandas as pd


def get_objs(layout, results):
    if not isinstance(layout, LTContainer):
        return
    for obj in layout:
        if isinstance(obj, LTTextLine):
            results.append({'bbox': obj.bbox, 'text' : obj.get_text(), 'type' : type(obj)})
        get_objs(obj, results)


def main(path):
    with open(path, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # https://pdfminersix.readthedocs.io/en/latest/api/composable.html#
        laparams = LAParams(
            all_texts=True,
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            print('objs-------------------------')
            get_objs(layout, results)
            for r in results:
                print(r)


PDF_DIR = './pdfs/'
pdfs = os.listdir(PDF_DIR)
pdfs.sort()

df = tabula.read_pdf(PDF_DIR + pdfs[-1], lattice=True, pages ='all')

df[0].shape

main(PDF_DIR + pdfs[0])

# +
tables = camelot.read_pdf(PDF_DIR + pdfs[0])

# for ix in tables[0].df.index:
#     print(ix, tables[0].df.loc[ix][0], '|', tables[0].df.loc[ix][1])
# -

for ix in tables[0].df.index:
    tb = tables[0].df
    col = tb.shape[1]
    li = [tables[0].df.loc[ix][r] for r in range(0,col)]
    print(' | '.join(li))

tables[0].df.loc[2] [1].split('\n')


def exTextPdf(fPath):
    f = open(fPath, 'rb')
    outf = StringIO()    
    rm = PDFResourceManager()
    lap = LAParams()
    dev = TextConverter(rm, outf, laparams=lap)
    iprlr = PDFPageInterpreter(rm, dev)
    for page in PDFPage.get_pages(f):
        iprlr.process_page(page)
    contents = outf.getvalue()
    outf.close()
    dev.close()
    f.close()
    return contents.split('\n')


fPath = PDF_DIR + pdfs[0]

exTextPdf(fPath)

fPath1 = PDF_DIR + pdfs[-1]
exTextPdf(fPath1)










