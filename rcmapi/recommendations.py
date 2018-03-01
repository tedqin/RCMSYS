#encoding:utf-8
# -*- coding:utf-8 -*-
from math import sqrt
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('gbk')

_path = sys.path

##########################################################################基于用户的过滤####################################3
#欧几里得距离
def sim_distance(prefs,person1,preson2):
    si={}
    for item in prefs[person1]:
        if item in prefs[preson2]:
            si[item]=1
    if len(si)==0:return 0
    n=len(si)
    #printn
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[preson2][item],2) for item in prefs[person1] if item in prefs[preson2]])
    return 1/(1+sqrt(sum_of_squares))

#皮尔逊距离
def sim_pearson(prefs,p1,p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    n=len(si)
    if n==0:
        return 1

    #所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    #所有偏好求平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    #乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    #计算皮尔逊相关系数
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

    if den==0:
        return 0
    r=num/den
    return r

#对person计算出相似的有关人员和相似度评价值
# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other)for other in prefs if other != person]
    # 参见列表推导式
    # 对列表排序，评价值最高的排在前面
    scores.sort() # 排序
    scores.reverse() # 反向列表中元素
    return scores[0:n]


#对person使用pearson协同过滤得到推荐
# 利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity = sim_pearson):
    totals = {}
    simSums = {}
    sim_list = {}
    i = 1
    for other in prefs:
        # 不要和自己作比较
        if other == person: continue
        sim = similarity(prefs, person, other)
        sim_list[other] = sim
    sorted(sim_list.items(), key=lambda x: x[1], reverse=True)

    iter = 0
    for other in sim_list:
        if iter > 30:
            break
        iter += 1
        # 不要和自己作比较
        if other ==person: continue
        sim = similarity(prefs, person, other)
        #忽略评价值为零或小于零的情况
        if sim <= 0: continue
        for item in prefs[other]:
            #只对自己还没看过的书籍评价
            if item not in prefs[person] or prefs[person][item] == 0:
                # 相似度 * 评价值
                totals.setdefault(item, 0)
                # setdefault() 函数: 如果键不已经存在于字典中，将会添加键并将值设为默认值。
                # dict.setdefault(key, default=None)
                # key -- 查找的键值。
                # default -- 键不存在时，设置的默认键值。
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim
            i+=1

    # 建立一个归一化的列表
    rankings = [(total / simSums[item], item) for item, total in totals.items()] # 列表推导式
    # 返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings

#得到与prefs商品相近的商品
#这个函数就是将字典里面的人员和物品对调
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      result[item][person]=prefs[person][item]
  return result


##########################################################################基于物品的过滤####################################
#得到不同物品以及与该物品相似的其他物品的矩阵
def calculateSimilarItems(prefs, n = 10):
    # 建立字典，以给出与这些物品最为相近的所有其他物品
    result = {}
    # 以物品为中心对偏好矩阵实施倒置处理
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # 针对大数据集更新状态变量
        c += 1
        if c % 100 == 0:print ("%d / %d" % (c, len(itemPrefs)))
        # 寻找最为相近的物品
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores
    return result # 返回一个包含物品及其最相近物品列表的字典

#基于物品推荐
def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    #循环遍历与当前物品相近的物品
    for (item,rating) in userRatings.items():

        for (similarity,item2) in itemMatch[item]:
            #如果该用户已经对当前物品做出过评价，就忽略
            if item2 in userRatings:continue

            #评价值与相似度的加权之和
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    #将每个和值除以加权和，求平均值
    rankings=[(score/totalSim[item],item) for item,score in scores.items()]

    #排序
    rankings.sort()
    rankings.reverse()
    return rankings

def loaddata(path):
    books={}
    for line in open(path+'list.csv'):
        (id,title)=line.split(',')[0:2]
        books[id]=title

    # Load data
    prefs={}
    for line in open(path+'rating.csv'):
        (user,bookid,rating)=line.split(',')
        prefs.setdefault(user,{})
        prefs[user][books[bookid]]=float(rating)
    return prefs

def loaditem(path):
    # 存储itemsim字典
    # f_item = open('itemsim.model', 'w')
    # f_item.write(str(itemsim))
    # f_item.close()
    #读取itemsim字典
    f_item = open(path+'itemsim.model', 'r')
    a = f_item.read()
    itemsim = eval(a)
    f_item.close()
    return itemsim

def ranking(path):
    rank_list = []
    with open(path+'test.txt', 'r') as f:
        for line in f.readlines():
            rank_list.extend(line.split())
    #print(Counter(rank_list))
    most_ranking = Counter(rank_list).most_common(10)

    books = {}
    for line in open(path + 'list.csv'):
        (id,title)=line.split(',')[0:2]
        books[id]=title
    #print(most_ranking[0][0])
    #print(books[most_ranking[0][0]])
    f_rank = open('book.ranking', 'w')
    f_rank.write(str(most_ranking))
    #f_rank.write(books[most_ranking[0][0]])
    f_rank.close()

    return most_ranking

def load_rank(path):
    rank_list = []
    with open(path+'rank.txt', 'r') as f:
        for line in f.readlines():
            rank_list.extend(line.split('\r\n'))
    #print(Counter(rank_list))
    return rank_list


if __name__ == '__main__':
    pass