import surprise
import pandas as pd
import tkinter
import numpy as np
import math


ratings_expand = {
    '마동석': {
        '택시운전사': 3.5,
        '남한산성': 1.5,
        '킹스맨:골든서클': 3.0,
        '범죄도시': 3.5,
        '아이 캔 스피크': 2.5,
        '꾼': 3.0,
    },
    '이정재': {
        '택시운전사': 5.0,
        '남한산성': 4.5,
        '킹스맨:골든서클': 0.5,
        '범죄도시': 1.5,
        '아이 캔 스피크': 4.5,
        '꾼': 5.0,
    },
    '윤계상': {
        '택시운전사': 3.0,
        '남한산성': 2.5,
        '킹스맨:골든서클': 1.5,
        '범죄도시': 3.0,
        '꾼': 3.0,
        '아이 캔 스피크': 3.5,
    },
    '설경구': {
        '택시운전사': 2.5,
        '남한산성': 3.0,
        '범죄도시': 4.5,
        '꾼': 4.0,
    },
    '최홍만': {
        '남한산성': 4.5,
        '킹스맨:골든서클': 3.0,
        '꾼': 4.5,
        '범죄도시': 3.0,
        '아이 캔 스피크': 2.5,
    },
    '홍수환': {
        '택시운전사': 3.0,
        '남한산성': 4.0,
        '킹스맨:골든서클': 1.0,
        '범죄도시': 3.0,
        '꾼': 3.5,
        '아이 캔 스피크': 2.0,
    },
    '나원탁': {
        '택시운전사': 3.0,
        '남한산성': 4.0,
        '꾼': 3.0,
        '범죄도시': 5.0,
        '아이 캔 스피크': 3.5,
    },
    '소이현': {
        '남한산성': 4.5, 
        '아이 캔 스피크': 1.0,
        '범죄도시': 4.0
    }
}

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
    
    avg_name1 = avg_name1 / count
    avg_name2 = avg_name2 / count
    
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for game in data[name1]:
        if game in data[name2]:
            sum_name1 += pow(data[name1][game] - avg_name1, 2)
            sum_name2 += pow(data[name2][game] - avg_name2, 2)
            sum_name1_name2 += (data[name1][game] - avg_name1) * (data[name2][game] - avg_name2)
    
    return sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2))



def msd(data, name1, name2):
    sum = 0
    count = 0
    for game in data[name1]:
        if game in data[name2]: 
            sum += pow(data[name1][game]- data[name2][game], 2)
            count += 1

    return 1 / ( 1 + (sum / count) )



def top_match(data, name, index=3, function=pearson):
    list=[]
    for i in data: 
        if name!=i: 
            list.append((function(data,name,i),i)) #상관계수를 리스트에 추가
    list.sort() 
    return list[:index]


def getRecommendation (data, person, k=3, function=pearson):
    
    result = top_match(data, person, k)
    
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



list=[]
#list=getRecommendation(ratings_expand, '소이현')
list = getRecommendation(ratings_expand, '최홍만', k=5, function=msd)
for items in list:
    print(items)