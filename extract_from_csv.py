import pandas as pd
import os
import csv
import re

COUNTY_NAME = 'brevard county'

cty_dir = './output_parseable/' + COUNTY_NAME
f = open(cty_dir + '/failed_parse.txt', 'w')
outp = csv.writer(open(cty_dir + '/loma_output.csv','w', newline=''), delimiter=',')
ftd = csv.reader(open('file_to_date.csv', 'r', newline=''), delimiter=',')

outp.writerow(['County', 'File Number', 'File Date', 'LOMA Type', 'Map Panel Number', 'Lot', 'Block/Section', 'Subdivision', 
    'Street', 'Outcome', 'Flood Zone', '1% Flood Elevation', 'Adjacent Grade Elevation', 'Lowest Lot Elevation'])

file_to_date = {}
for row in ftd:
    file_to_date[row[0]] = row[1]

for file in os.listdir(cty_dir):
    if file.endswith('.xlsx'):
        try:
            df = pd.read_excel(os.path.join(cty_dir, file), header=None)
            file_number = file.replace('.xlsx','')
            file_date = file_to_date[file_number]

            num_rows, num_cols = df.shape
            data_rows = set()

            loma_type = ''
            panel_num = ''
            for r in range(num_rows):
                if len(df.iloc[r,:].dropna()) == 9:
                    data_rows.add(r)
                for c in range(num_cols):
                    cell_val = str(df.iloc[r, c]).strip().replace('\n',' ')
                    if not loma_type and ('LOMA' in cell_val or 'LOMR' in cell_val) and len(cell_val) < 15:
                        loma_type = cell_val
                    
                    if not panel_num and 'NUMBER: ' in cell_val and len(cell_val) < 80:
                        panel_num = cell_val[cell_val.find('NUMBER: ') + 8:].strip()

            
            header_rows = set()
            for r in data_rows:
                header_ct = 0
                for c in range(num_cols):
                    cell_val = str(df.iloc[r, c]).strip().replace('\n',' ')
                    if (cell_val == 'LOT' or ('BLOCK' in cell_val and 'SECTION' in cell_val) or cell_val == 'SUBDIVISION' or cell_val == 'STREET' 
                        or 'OUTCOME' in cell_val or cell_val == 'FLOOD ZONE' or 'CHANCE FLOOD' in cell_val or 'ADJACENT GRADE' in cell_val
                        or 'LOWEST LOT' in cell_val):
                        header_ct += 1

                if header_ct > 2:
                    header_rows.add(r)

            data_rows -= header_rows
            if len(data_rows) <= 0 or len(data_rows) < len(header_rows):
                raise Exception('Not enough data found')

            for r in data_rows:
                output_row = [COUNTY_NAME.title(), file_number, file_date, loma_type, panel_num]
                for c in range(num_cols):
                    if not pd.isna(df.iloc[r, c]):
                        cell_val = str(df.iloc[r, c]).strip().replace('\n',' ')
                        if re.match('^[.-]+$', cell_val):
                            cell_val = '--'
                        output_row.append(cell_val)
                print(output_row)
                outp.writerow(output_row)

        except Exception as e:
            f.write(file_number+'\n')
            print(e)
