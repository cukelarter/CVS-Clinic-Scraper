# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 01:11:31 2022

@author: cukel
"""


import pandas as pd

infeed=pd.read_json(r'C:\Users\cukel\OneDrive\Documents\upwork\cvsclinic\fullcrawl.json')


infeed['services']=infeed['services'].apply(lambda x: "\n".join(x))

writer=pd.ExcelWriter(r'C:\Users\cukel\OneDrive\Documents\upwork\cvsclinic\testfile2.xlsx')
infeed.to_excel(writer, sheet_name='cvsclinics', index=False)
worksheet = writer.sheets['cvsclinics']
# auto adjust row width
#for index, row in infeed.iterrows():
##    row_height=max(row.astype(str).map(len).max(),len(row))
#    worksheet.set_row(1, 1, row_height)
worksheet.set_row(2,45)

writer.save()




#%% Testing

tester=['cock','ball','torture']

print(tester)

print("\n".join(tester))