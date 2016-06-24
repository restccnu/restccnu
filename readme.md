# restccnu
![piped-piper](http://7xj431.com1.z0.glb.clouddn.com/0_thumb.jpg)
华师校园通后台

## Mock
[已Mock的API: 主要的GET请求API]<br/>
[IP: 47.89.28.131:5060]

+ mock::/api/info/login/ -> 模拟登录信息门户
+ mock::/api/lib/login/ -> 模拟登录图书馆
+ mock::/api/lib/search/ -> 图书查询API(没有模拟分页和实际查询)
+ mock::/api/lib/<int:id>/ -> 图书详情API
+ mock::/api/lib/me/ -> 个人图书馆界面
+ mock::/api/table/ -> 个人课表API

## Apis
[已完成的API] <br/>
[IP: 47.89.28.131:5070]

1. **模拟登录部分**
    + API::/api/info/login/                             -> 模拟登录信息门户(部署)
    + API::/api/lib/login/                              -> 模拟登录图书馆(部署)
2. **图书馆部分**
    + API::/api/lib/search/?keyword=xxx&page=1          -> 图书搜索API
    + API::/api/lib/?id=xxx&book=xxx&author=xx          -> 图书详情API
    + API::/api/lib/me/                                 -> 我的图书馆API
3. **课表部分**
    + API::/api/table/?xnm=2015&xqm=3&sid=2014210761    -> 获取课表API
