import os
from shutil import copy2
import pdftotext

NEWPATH = './output_parseable'
OLDPATH = './output'

if not os.path.exists(NEWPATH):
    os.mkdir(NEWPATH)

# loop through all counties
for county in os.listdir(OLDPATH):
    print(county)
    old_county_path = os.path.join(OLDPATH, county)
    new_county_path = os.path.join(NEWPATH, county)
    if not os.path.exists(new_county_path):
        os.mkdir(new_county_path)

    # loop through every pdf file
    for file in os.listdir(os.path.join(OLDPATH, county)):
        if file.endswith('.pdf'):
            old_file_path = os.path.join(old_county_path, file)
            new_file_path = os.path.join(new_county_path, file)

            # if not already in new path, open pdf as text
            if not os.path.exists(new_file_path):
                with open(old_file_path, 'rb') as f:
                    try:
                        pdf = pdftotext.PDF(f)
                        text = "\n\n".join(pdf)
                        print(len(text))

                        # copy pdf to new path only if it contains text
                        if len(text) > 200:
                            copy2(old_file_path, new_county_path)
                    except:
                        print("Failed to open")