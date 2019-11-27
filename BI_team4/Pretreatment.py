import pandas as pd 
import math

data = pd.read_csv("./g.csv", encoding='CP949')

list(data)

data.columns

data=data.drop('타임스탬프',axis=1)

data

data_dict = {}

temp = float('nan')

for i in range(len(data)):
    temp_dict = {}
    for _list in list(data):
        # print(_list)
        if not math.isnan(data[_list][i]):
            temp_dict[_list]=data[_list][i]
    data_dict[i]=temp_dict

data_dict
