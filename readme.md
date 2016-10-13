<p align="center">
  <img src="https://avatars1.githubusercontent.com/u/22377500?v=3&s=200" width="60" /><br>RestCCNU<br>{华师匣子API}</br>
</p>

## $-部署流程(docker, docker-compose)
### 1. 配置环境
编写 ```restccnu.env```, 配置项如下: <br/>

+ REST_MONGO_HOST: mongodb数据库 host ip
+ QINIU_EMAIL: 七牛账号
+ QINIU_PASS: 七牛密码
+ QINIU_ACCESS_KEY: 七牛账号公钥
+ QINIU_SECRET_KEY: 七牛账号私钥
+ QINIU_BUCKET_NAME: 七牛bucket名称
+ QINIU_BUCKET_DOMAIN: 七牛bucket域名
+ ADMIN_EMAIL: 管理员账号
+ ADMIN_PASS: 管理员密码
+ C_FORCE_ROOT: (true) root运行celery
+ CELERY_ACCEPT_CONTENT: (json) pickle root运行celery有漏洞

### 2. 部署运行
部署运行命令:

    $ git clone https://github.com/restccnu/restccnu
    $ docker-compose build
    $ docker-compose up -d (后台运行)
    $ docker-compose logs (查看log)

运行在ip:5486端口(如果是Mac且不是docker for mac, ip就是docker-machine ip)

## $-运行测试
### 本地测试(docker, unittest)
本地测试运行在docker中(docker-compose.test.yml), 确保测试环境和部署环境完全一致. <br/>

**1.配置环境(除部署配置项外, 还需)** <br/>

+ USER_NAME: 你的信息门户学号
+ USER_PASS: 你的信息门户密码

**2.运行本地测试**

    $ sh shell/restccnu_test.sh

### 集成测试(docker, travis-ci)
pass
<br/>

+ 测试覆盖见[ISSUE37](https://github.com/restccnu/restccnu/issues/37)

## $-restccnu架构图
![restccnu架构](https://cloud.githubusercontent.com/assets/10671733/19296662/fcbfccb6-906f-11e6-8c03-adbe5e3e5ba9.png)

## $-nginx负载均衡分布
(团队3台server)

### 模拟登录负载

+ **入口Server**: 123.56.41.13 <- ccnubox.muxixyz.com
    - 123.56.41.13
    - 120.25.166.213
    - 121.42.176.189 (备用:自己的服务器)

### 成绩查询负载

+ **入口Server**: 120.25.166.213 <- grade.muxixyz.com
    - 120.25.166.213
    - 121.42.176.189

### 课表查询负载

+ **入口Server**: 123.56.41.13 <- ccnubox.muxixyz.com
    - 123.56.41.13 (weight=3)
    - 218.199.196.131 (备用:学校恶心的服务器)

## $-项目组织结构

- ```fuckccnu```: 反反爬虫
    - IPool: 代理池(没写)
    - multiUA: userAgent模拟(300+userAgent)
- ```mock```: 虚拟数据
- ```server```: 服务器配置
    - nginx: 前端代理服务器
    - gunicorn: 后端服务器
- ```shell```: 使用到的shell脚本
    - docker_deploy.sh: docker部署脚本
    - mongobackup.sh: mongodb数据库备份脚本
    - supervisor_deploy.sh: supervisor部署脚本(已停止使用)
- ```supervisor```: supervisor进程监控配置(已停止使用)
- ```restccnu```: 核心代码
    - ```apis```: api
    - ```models```: 数据库
    - ```spiders```: 爬虫
    - ```workers```: celery定时任务
- ```tests```: 测试(没写)
- ```config.py```: 项目配置

## $-API文档

+ https://goo.gl/9lU47K

## $-华师匣子下载

+ https://ccnubox.muxixyz.com/

## $-备注

+ **2016年10月12日**
    - restccnu重构
+ **2016年10月**
    - 华师匣子主服务ship on docker:)
+ **2016年9月**
    - 由于访问量太大, 学校关闭外网访问, 导致部分API无法使用.(现已恢复)

## $-Built with ❤️  and MuxiStudio
![railgun](https://avatars3.githubusercontent.com/u/10671733?v=3&s=466)
