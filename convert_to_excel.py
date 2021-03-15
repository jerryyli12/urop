import win32com.client, win32com.client.makepy, os, winerror, pandas as pd, errno, re
from win32com.client.dynamic import ERRORS_BAD_CONTEXT

# excel_file = "output.xlsx"

# ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)

# src = os.path.abspath('17-04-1924A-120419.pdf')

# win32com.client.makepy.GenerateFromTypeLibSpec('Acrobat')
# adobe = win32com.client.DispatchEx('AcroExch.App')
# avDoc = win32com.client.DispatchEx('AcroExch.AVDoc')
# avDoc.Open(src, src)
# pdDoc = avDoc.GetPDDoc()
# jObject = pdDoc.GetJSObject()
# jObject.SaveAs(excel_file, "com.adobe.acrobat.xlsx")
# avDoc.Close(-1)

ALL_DIR = './output_parseable/'
ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)
win32com.client.makepy.GenerateFromTypeLibSpec('Acrobat')
adobe = win32com.client.DispatchEx('AcroExch.App')
avDoc = win32com.client.DispatchEx('AcroExch.AVDoc')

for county in os.listdir(ALL_DIR):
    cty_dir = os.path.join(ALL_DIR, county)
    for file in os.listdir(cty_dir):
        if file.endswith('.pdf'):
            file_number = file.replace('.pdf','')
            file_path = os.path.abspath(os.path.join(cty_dir, file))

            excel_file = file_number + '.xlsx'
            if os.path.exists(os.path.join(cty_dir, excel_file)):
                continue

            print("file_path", file_path)

            avDoc.Open(file_path, file_path)
            pdDoc = avDoc.GetPDDoc()
            jObject = pdDoc.GetJSObject()
            jObject.SaveAs(excel_file, "com.adobe.acrobat.xlsx")
            avDoc.Close(-1)
