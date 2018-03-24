# spider
用urllib2和BeautifulSoup来爬取豆瓣上的电影信息，并将其存储到数据库中
# 依赖库和软件
## bs4 
主要依赖该库中的BeautifulSoup，利用其来解析HTML,进而从中提取信息。
安装命令：<br>  
```shell
sudo pip install bs4
```
## urllib2
主要利用该库来连接url获取html页面,另外还使用了其中的代理功能。一般python默认自带urllib2库。
## lxml
BeautifulSoup中使用lxml作为HTML解析引擎。
安装命令：<br>  
```shell
sudo pip install lxml
```
## mysql
本工程采用mysql作为存储数据库，当从页面抓取相关信息时，程序自动将其存入数据库。
安装命令：<br>  
```shell
sudo apt-get install mysql-server 
sudo apt-get isntall mysql-client
sudo apt-get install libmysqlclient-dev  
```
安装完后设置密码和创建数据库即可

## MySQL-python
用于python连接并操作mysql数据库。
安装命令：<br>  
```shell
sudo pip install MySQL-python
```
# 数据库相关配置
```python
host = 'localhost'
user = 'root'
password = 'admin'
database = 'test'
```
# 使用说明
```python
runSpider(tag = ['电影'],startPage = 0,Pagenum = 1000,size = 100)
tag：        为内容标签
startPage：  为起始页
PageNum：    为页面数量
size：       为抓取size个链接后，才开始抓取相关详细信息。
```
```python
例子：
runSpider()
```
# 代理
为了防止豆瓣的反爬虫机制，本程序采用代理服务器进行爬虫。从西刺网上获取免费的HTTPS高匿代理服务器地址和端口，
获取的方式也是采取爬虫，获取并解析页面上的信息。在获得代理信息时，还需要对其进行验证，测试其是否可用。最后
只保留可用代理。<br>
程序首先获取一个代理池，此过程由于要验证代理服务器，需要时间可能较长。获取代理池后，每过一段时间就从代理池
中获取一个代理，然后用该代理去访问豆瓣网，这样就可以隐藏自己的IP，避免自己的IP被封。
