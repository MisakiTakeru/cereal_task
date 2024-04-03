import pandas as pd
import matplotlib.pyplot as plt
import operator as op
import os

file = 'C:/Users/KOM/Documents/git/cereal_task/data/Cereal.csv'
df = pd.read_csv(file, sep = ';', header = 0, skiprows = [1], on_bad_lines = 'skip')
df = df.drop('rating', axis = 1)
"""
Parameters
----------
cat : string
    one of the categories in the dataframe
op_type : string
    an operator function from pythons operator package
    possible calls are :
        lt, le, eq, ne, ge ,gt
cond : string or int or float
    the condition which the data is compared to
    
uses getattr to get the operator functions from the package operator and
applies it to the type from the dataframe category and the condition.
"""
def filter_df(cat, op_type, cond):
    return df.loc[getattr(op, op_type)(getattr(df,cat), cond)]



"""
Parameters
----------
ids : int
    id for a given product
"""
def get_image(ids):
# Gets the img file names, and creates a version that has turned all
# characters lowercase and removed whitespace for easier comparison
    for _, _, files in os.walk('data/Cereal pictures'):
        filenames = files
        filenames2 = [x.lower().replace(' ','') for x in files]
    try:
        n = df.at[ids, 'name']
    except Exception:
        raise KeyError(f'given key {ids} is out of bounds for our database')
# normalizes the name by removing white spaces and enforce lowercases
    n = n.lower().replace(' ','')
# There are both jpg and png files so we need to check for both
    if (n +'.jpg') in filenames2:
        i = filenames2.index((n +'.jpg'))
    elif (n + '.png') in filenames2:
        i = filenames2.index((n +'.png'))
# 1 image has a ',' instead of '.' in name
    elif (n.replace('.',',') + '.jpg') in filenames2:
        i = filenames2.index((n.replace('.',',') + '.jpg'))
# 1 image has a spelling error in name.
    elif n == 'muesliraisins,dates,&almonds':
        i = filenames2.index('muesliraisins,dates,&almons.jpg')
    else:
        print(f'We have no image for id {ids}')
        return False
    
    img_path = 'data/Cereal pictures/' + filenames[i]
    img = plt.imread(img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    return True
        
