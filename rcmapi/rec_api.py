#encoding:utf-8
import json
from recommendations import *
import os
import sys
reload(sys)
sys.setdefaultencoding('gbk')
_path = os.path.dirname(os.path.abspath(__file__)) + '\\..\\data\\sc\\'

def recbooks(_id):
    prefs = loaddata(_path)
    books=transformPrefs(prefs)

    dic = getRecommendations(prefs, _id)[0:30]
    base_user = dic  #基于用户推荐
    print ("base user",base_user)

    itemsim = loaditem(_path)
    base_item = getRecommendedItems(prefs, itemsim, _id)[0:30] #基于物品推荐
    print ("base item", base_item)

    ranklist = load_rank(_path) #前30热销
    print ("ranklist", ranklist)

    return base_user,base_item,ranklist

if __name__ == "__main__":
    recbooks('9461X77')