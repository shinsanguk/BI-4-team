import surprise
import pandas as pd
import tkinter
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")

#피어슨 유사도
def pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for game in data[name1]:
        if game in data[name2]:
            avg_name1 = data[name1][game]
            avg_name2 = data[name2][game]
            count += 1
    if count != 0:
        avg_name1 = avg_name1 / count
        avg_name2 = avg_name2 / count
    else:
        return
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for game in data[name1]:
        if game in data[name2]:
            sum_name1 += pow(data[name1][game] - avg_name1, 2)
            sum_name2 += pow(data[name2][game] - avg_name2, 2)
            sum_name1_name2 += (data[name1][game] - avg_name1) * (data[name2][game] - avg_name2)
    
    ps = (sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2)))
    return ps



def msd(data, name1, name2):
    sum = 0
    count = 0
    for game in data[name1]:
        if game in data[name2]: 
            sum += pow(data[name1][game]- data[name2][game], 2)
            count += 1

    return 1 / ( 1 + (sum / count) )



def top_match(data, name, index=81, function=pearson):
    list=[]
    for i in data: 
        if name!=i: 
            list.append((function(data,name,i),i)) #상관계수를 리스트에 추가

    try:
        list.sort()
        
    except TypeError :
       
        print("데이터 부족")
        return []
        
    return list[:index]


def getRecommendation (data, person, k=3, function=pearson):
    
    result = top_match(data, person, k,function)
    
    score = 0 
    list = [] 
    score_dic = dict() 
    sim_dic = dict() 

    for sim, name in result: 
        print(sim, name)
        if sim < 0 : continue 
        for game in data[name]: 
            if game not in data[person]: 
                score += sim * data[name][game] 
                score_dic.setdefault(game, 0) 
                score_dic[game] += score 

                # 조건에 맞는 유사도의 누적합
                sim_dic.setdefault(game, 0) 
                sim_dic[game] += sim
            score = 0  
    
    for key in score_dic: 
        score_dic[key] = score_dic[key] / sim_dic[key] # 평점 총합/ 유사도 총합
        list.append((score_dic[key],key))
    list.sort() 
    return list


data = pd.read_csv("./g.csv", encoding='CP949')
list(data)
data=data.drop('타임스탬프',axis=1)
data_dict = {}
temp = float('nan')

for i in range(len(data)):
    temp_dict = {}
    for _list in list(data):
        # print(_list)
        if not math.isnan(data[_list][i]):
            temp_dict[_list]=data[_list][i]
    data_dict[i]=temp_dict

list=[]

list=getRecommendation(data_dict, 1,k=5)

max=0
item=""
for item in list:
   if item[0] >max:
       max = item[0]
       name = item[1]

print(str(item[0])+" "+item[1])