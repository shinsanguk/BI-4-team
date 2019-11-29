#!/usr/bin/env python
# coding: utf-8

# In[14]:


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
    alist=[]
    for i in data: 
        if name!=i: 
            alist.append((function(data,name,i),i)) #상관계수를 리스트에 추가

    try:
        alist.sort()
        
    except TypeError :
       
        print("데이터 부족")
        return ["데이터 부족"]
        
    return alist[:index]


def getRecommendation (data, person, k, function=pearson):
    
    result = top_match(data, person, k,function)
    
    score = 0 
    nlist = [] 
    score_dic = dict() 
    sim_dic = dict() 
    
    if result == ["데이터 부족"]:
        return ["데이터 부족"]
    else:
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
            nlist.append((score_dic[key],key))
        nlist.sort() 
        return nlist


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


# In[23]:


import tkinter

window=tkinter.Tk()
window.title("Game recomm. sys.")
window.geometry("1000x500+100+100")
window.resizable(False, False)

rating = [
    '1', '2', '3', '4', '5'
]

gamelist = [
    ' [스타크래프트 (starcraft)]',
    ' [롤 (league of legends)]',
    ' [메이플스토리 (maple story)]',
    ' [오버워치 (OverWatch)]',
    ' [서든어택 (Sudden Attack)]',
    ' [배틀그라운드 (PUBG)]',
    ' [마인크래프트 (MineCraft)]',
    ' [던전 앤 파이터 (Dungeons & Fighters)]',
    ' [포트나이트 (Fortnite)]',
    ' [카트라이더 (Cart Rider)]',
    ' [월드 오브 워크래프트 (WoW)]',
    ' [사이퍼즈 (Cyphers)]',
    ' [하스스톤 (Hearth Stone)]',
    ' [디아블로 (Diablo)]',
    ' [GTA]',
    ' [리니지 (Lineage)]',
    ' [검은사막 (Black Desert)]',
    ' [크레이지아케이드 (Crazy Arcade)]',
    ' [카운터스트라이크 (Counter Strike)]',
    ' [피파온라인 (FIFA Online)]',
    ' [블레이드 앤 소울 (Blades & Souls)]',
    ' [FM]',
    ' [로스트아크 (Lostark)]',
    ' [포켓몬고 (Pokemon GO)]',
    ' [앵그리버드 (angry bird)]'
]

donelist = []
ratinglist = []
chkbtlist = []
dropbutton = []
ratingval = []
namelabel = []

def dropcall(*args):
    for i in range(len(gamelist)):
        ratingval[i] = int(ratinglist[i].get())
        
def chckcall(*args):
    for i in range(len(gamelist)):
        if donelist[i].get() == 0:
            dropbutton[i].config(state="disabled")
        else:
            dropbutton[i].config(state="active")
    

for i in range(len(gamelist)):
    ratingval.append(0)
    ratinglist.append(tkinter.StringVar())
    ratinglist[i].set(rating[0])
    donelist.append(tkinter.IntVar(value=1))
    namelabel.append(tkinter.Label(window, text=gamelist[i]))
    chkbtlist.append(tkinter.Checkbutton(window, variable=donelist[i]))
    #chkbtlist[i].select()
    dropbutton.append(tkinter.OptionMenu(window, ratinglist[i], *rating))
    rowp = i / 5
    colp = i % 5
    namelabel[i].grid(row=3*int(rowp), column=int(colp))
    chkbtlist[i].grid(row=3*int(rowp)+1, column=int(colp))
    chkbtlist[i].config(width=10)
    dropbutton[i].grid(row=3*int(rowp)+2, column=int(colp))
    dropbutton[i].config(width=10)
    ratinglist[i].trace("w", dropcall)
    donelist[i].trace("w", chckcall)
    
label=tkinter.Label(window, text="")



def pret(*args):
    inputdict = {}
    for i in range(len(gamelist)):
        if donelist[i].get() == 1:
            inputdict[gamelist[i]] = int(ratinglist[i].get())
    return inputdict

def runrec(*args):
    label.config(text="On calc...")
    global data_dict
    totaldata = dict(data_dict)
    totaldata[82] = pret()
    alist=[]
    
    rec = "Not enough data" 
    alist=getRecommendation(totaldata, 82, k=5)
    if not alist == ["데이터 부족"]:
        for game in alist:
            #if game[1] in totaldata[82]:
            rec = game[1]
    

    label.config(text="Recommendataion: " + rec)

button = tkinter.Button(window, overrelief="solid", width=50, repeatdelay=1000, repeatinterval=100, text="Run!", command=runrec)
button.grid(columnspan=5)
label.grid(columnspan=5)

window.mainloop()


# In[ ]:





# In[ ]:




