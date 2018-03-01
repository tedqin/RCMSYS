## 上创项目-flask-基于协同过滤的图书推荐系统

### flask1.0.2+python2.7

### 运行： ``./start.sh``

### 前端
* Adduser.html：新用户注册
* Base.html：主体背景
* Books.html：推荐页面
* Getid.html：获取id页面
* Index.html：主页面

### 后端
* RCM-Front.py：路由配置页面
* Rec_api：api
* Recommendations.py：后台处理脚本，实现推荐算法和其他功能
![](https://i.imgur.com/Diepeh8.png)
后端主要目的是实现两种协同过滤算法，基于用户和基于物品。根据调查，我们发现学校图书馆网站已经推出了图书评分（评星级）系统，所以我们将评分制度加入进了推荐系统并且基于用户的评分实现更精准的推荐。

### index
![](https://i.imgur.com/qQzDCp0.png)

### getid
![](https://i.imgur.com/Si4F50G.png)

### book
![](https://i.imgur.com/KbTEOWP.png)
