import pandas as pd
import matplotlib.pyplot as plt
import operator as op
import os
import functools

file = 'C:/Users/KOM/Documents/git/cereal_task/data/Cereal.csv'
df = pd.read_csv(file, sep = ';', header = 0, skiprows = [1], on_bad_lines = 'skip')
df = df.drop('rating', axis = 1)
"""
Parameters
----------
cat : string or [string]
    the categories in the dataframe
op_type : string or [string]
    operator functions from pythons operator package
    possible calls are :
        lt, le, eq, ne, ge ,gt
cond : string or int or float or list of string, int and float
    the condition which the data is compared to
    
uses getattr to get the operator functions from the package operator and
applies it to the type from the dataframe category and the condition.
"""
def filter_df(cat = None, op_type = None, cond = None):
    if cat == None:
        return df
    if type(cat) == list and type(op_type) == list and type(cond) == list:
        if len(cat) != len(op_type) or len(cat) != len(cond):
            raise AttributeError('all input values must be of same length')
# creates a list of mapped conditions, and then ands them all together to allow
# multiple filtering conditions.
        mapped = list(map(lambda c, o, con : getattr(op, o)(getattr(df,c), con), cat, op_type, cond))
        return df.loc[functools.reduce(lambda x, y : x & y, mapped)]
    elif type(cat) == list or type(op_type) == list or type(cond) == list:
        raise AttributeError('all input values must either be a single input or list')
    else:
        return df.loc[getattr(op, op_type)(getattr(df,cat), cond)]

"""
Parameters
----------
ids : int
    The id that will be updated

cat : string
    The category that will be updated on the ids
vals : variable
    What the category will be updated by
"""
def update(ids, cat, vals):
    if type(cat) == list and type(vals) == list:
        new_df = pd.DataFrame(dict(map(lambda k, v : (k,v) , cat, vals)), index = [ids])
    else:
        new_df = pd.DataFrame({cat : vals}, index = [ids])
    df.update(new_df)
    

"""
Parameters
----------
name, mfr, types : string

calories, protein, fat, sodium, sugars, potass, vitamins, shelf : integer

fiber, carbo, weight, cups : float
"""
def add_row(name, mfr, types, calories, protein, fat, sodium, fiber, carbo, sugars,
            potass, vitamins, shelf, weight, cups):
    cats = ['name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 'fiber',
           'carbo', 'sugars', 'potass', 'vitamins', 'shelf', 'weight', 'cups']
    vals = [name, mfr, types, calories, protein, fat, sodium, fiber, carbo, sugars,
                potass, vitamins, shelf, weight, cups]
    new_row = dict(map(lambda k, v : (k,v) , cats, vals))
    df.loc[len(df)] = new_row
    return df

def delete(df, ids):
    return df.drop(ids, axis = 0)

"""
Parameters
----------
ids : int
    id for a given product

gets the name of the id given, and then checks if there exists a image
corresponding to the name and if there is shows it and returns True
otherwise it returns false.
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
        
