# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:39:27 2020

@author: TimK
"""

import pandas as pd
import datetime 



# dd/mm/YY
d1 = datetime.datetime.today().strftime("%d/%m/%Y")
Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
prev_d1 = Previous_Date.strftime ('%d/%m/%Y')

df = pd.read_csv('C:/Users/TimK/Documents/ds_housing_proj/rightmove2.csv')

df = df[df['Price']!= 'POA'] # Hide any prices that are not required
df = df[df['Property']!= 'Property']
df = df[df['Date Posted'].notnull()]

date_val = df['Date Posted'].apply(lambda x: x.split('on')[-1])
date_val = date_val.apply(lambda x: x.lower().replace('added today',str(d1)).replace('reduced today',str(d1)).replace('added yesterday', str(prev_d1)).replace('reduced yesterday', str(prev_d1)))
prop_type = df['Property'].apply(lambda x: x.split('for')[0]) # 'for sale' removed
minus_p = df['Price'].apply(lambda x: int(x.replace('£','').replace(',', ''))) # '£' removed
minus_ast = df['Description'].apply(lambda x: x.replace('***', '').replace('**', '').replace('*', '').replace('+++','')) # removing "***" from the description

df['Description'] = minus_ast
df['price_val'] = minus_p
# remove "for sale" from the 'Property column
df['Property'] = prop_type
df['Date Posted'] = date_val
# remove "£" sign and remove POA from Price
df['price_val'].dtype
# parsing of location 

# Luton
df['luton_yn'] = df['Address'].apply(lambda x: 1 if 'luton' in x.lower() else 0)
df.luton_yn.value_counts()
# Essex
df['essex_yn'] = df['Address'].apply(lambda x: 1 if 'essex' in x.lower() else 0)
df.essex_yn.value_counts()
# Braintree
df['braintree_yn'] = df['Address'].apply(lambda x: 1 if 'braintree' in x.lower() else 0)
df.braintree_yn.value_counts()
# parsing of description

#  garden
df['garden_yn'] = df['Description'].apply(lambda x: 1 if 'garden' in x.lower() else 0)
df.garden_yn.value_counts()
# planning/ extension 
df['exten_yn'] = df['Description'].apply(lambda x: 1 if 'exten' in x.lower() else 0)
df.exten_yn.value_counts()

df.to_csv('rm_data_cleaned.csv')

