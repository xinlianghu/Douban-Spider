# -*- coding: utf-8 -*-
import urllib2
import zlib
from bs4 import BeautifulSoup
import lxml
import re
import sys
import time
import random
import math
from moveinfo import *
import json
reload(sys)
sys.setdefaultencoding('utf-8')
req_headers = {
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip,deflate',
            #'Connection': 'keep-alive',
            #'Upgrade-Insecure-Requests': '1'
            }
UserAgent = ["Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:58.0) Gecko/20100101 Firefox/58.0",
             "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
             "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
             "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
             "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
             "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
             "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
             "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
             "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
             "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
             "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
             "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
             "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
             "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
             "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
             "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
             "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
             ]
proxyPool = []
def getHTML(proxy,url):
    url = url
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)
    header = req_headers.copy()
    header['User-Agent'] = selectUserAgent()
    request = urllib2.Request(url,headers=header)
    response = None
    try:
        response = opener.open(request,timeout = 3)
    except urllib2.URLError as e:
        errorcode = None
        reason = None
        if hasattr(e, 'code'):
            errorcode = e.code
        if hasattr(e, 'reason'):
            reason = e.reason
        return None,errorcode,reason
    except Exception as e:
        print e
        return None, None, None
    html = response.read()
    if response.headers['Content-Encoding'] == 'gzip':
        html = zlib.decompress(html,16+zlib.MAX_WBITS)
    return html,None,None

def getMovieInfo(html):
    movieInfo = {}
    soup = BeautifulSoup(html,'lxml')
    #name = soup.find('span',  property="v:itemreviewed").text
    #movieInfo['名字'] = str(name)

    year = soup.find('span',class_="year").text[1:-1]
    movieInfo['出品时间'] = str(year)
    info = soup.find('div',id='info').get_text()
    infolines = str(info).replace(':\n',':').lstrip().splitlines()
    for line in infolines:
        lineSplit = line.split(':')
        lineValue = ''
        for i in range(1,len(lineSplit)):
            lineValue += lineSplit[i]
        movieInfo[lineSplit[0]] = lineValue
    if soup.find('span' ,property="v:votes") != None:
        score = str(soup.find('strong' ,class_='ll rating_num').text)
        ratingNum = str(soup.find('span' ,property="v:votes").text)
        rating = [0] * 5
        parent = soup.find('div', class_="ratings-on-weight")
        items = parent.find_all('div', class_='item')
        index = 4
        for item in items:
            span = item.find_all('span')
            rating[index] = str(span[1].text.strip())
            index -= 1
        movieInfo['评分'] = rating
    else:
        score = '0.0'
        ratingNum = '0'
    movieInfo['总评分'] = score
    movieInfo['评分人数'] = ratingNum
    return movieInfo

def grabInfo(urlList,proxy):
    global proxyPool
    db,cursor = init_database()
    create_table(db,cursor)
    i = 0
    while i < len(urlList):
        item = urlList[i]
        movieinfo = None
        url = item['url']
        id = item['id']
        tag = item['tag']
        name = item['name']
        html ,errorcode,reason= getHTML(proxy,url)
        if html == None:
            print 'Get HTML from %s failed! ' % url,'Error code:',errorcode,'reason:',reason
            if errorcode == 404:
                i +=1
            else:
                proxy, proxyPool = getProxyFromPool()
            continue
        i += 1
        print 'Get HTML from %s success!'% url
        try:
            movieinfo = getMovieInfo(html)
            movieinfo['索引'] = id
            movieinfo['类别'] = tag
            movieinfo['名字'] = name
            print BasicInfo(movieinfo)
            save(db,cursor,BasicInfo(movieinfo))
            delay_time(2)
        except Exception as e:
            print e
            continue
    db.close()

def delay_time(t):
    delay= random.uniform(0,t)
    time.sleep(delay)

def getProxyPool():
    result = []
    for index in range(0,2):
        if index == 0:
            url = 'http://www.xicidaili.com/wn/'
        else:
            url = 'http://www.xicidaili.com/wn/%d'%(index)
        header = req_headers.copy()
        header['Host'] ='www.xicidaili.com'
        request = urllib2.Request(url ,headers=header)
        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except Exception as e:
            print e
            continue
        if response.headers['Content-Encoding'] == 'gzip':
            html = zlib.decompress(html,16+zlib.MAX_WBITS)
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find('table',id="ip_list").find_all('tr')
        num = len(trs)
        proxy = []
        for i in range(1,num):
            tds = trs[i].find_all('td')
            if str(tds[4].get_text()) == '高匿':
                proxy.append({str(tds[5].get_text()).lower():str(tds[5].get_text()).lower()+'://'+str(tds[1].get_text()+':'+tds[2].get_text())})
        for i in proxy:
            if proxyCheck(i):
                result.append(i)
    print 'proxy pool:',result
    return result

def selectProxy():
    global proxyPool
    num = len(proxyPool)
    index = int(random.uniform(0,num))
    print 'index',index
    return proxyPool[index]

def proxyCheck(proxy):

    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)
    request = urllib2.Request("https://movie.douban.com")
    try:
        response = opener.open(request,timeout=3)
        response.read()
    except:
        return False
    else:
        return True

def getProxyFromPool():
    global proxyPool
    proxy = selectProxy()
    i = 0
    while not proxyCheck(proxy):
        if i > len(proxyPool) * 2:
            proxyPool = getProxyPool()
            print 'get new proxyPool',proxyPool
        i = i+1
        proxy = selectProxy()
    print 'getProxyFromPool: select proxy:',proxy
    return proxy,proxyPool

def selectUserAgent():
    num = len(UserAgent)
    index = int(random.uniform(0, num))
    return UserAgent[index]

def printInfo(movieinfo):
    for key in movieinfo.keys():
        print key,movieinfo[key]


def runSpider(tag = ['电影'],startPage = 0,Pagenum = 1000,size = 100):
    tag = ['电影']
    pageSize = 20
    urllist = []
    counter = 0
    global  proxyPool
    proxyPool = getProxyPool()
    proxy, proxyPool = getProxyFromPool()
    j = startPage
    for i in range(0,len(tag)):
        while j <= Pagenum:
            #proxy = {'https':'123.56.223.224:6666'}
            print 'current proxy:',proxy
            url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%s&start=%d"%(tag[i],j*pageSize)
            httpproxy_handler = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(httpproxy_handler)
            request = urllib2.Request(url)
            try:
                response = opener.open(request,timeout=3)
                data = response.read()
                print 'grab succes Tag:%s Page:%d' % (tag[i], j)
                data = json.loads(data)
                for k in data['data']:
                    urllist.append({'id':str(k['id']),'url':str(k['url']),'tag':tag[i],'name':str(k['title'])})
                    print k['url']
                    counter += 1
                    if counter % size == 0:
                        grabInfo(urllist,proxy)
                        proxy, proxyPool = getProxyFromPool()
                        print 'select proxy:',proxy
                        urllist = []
                j +=1
                delay_time(2)
            except urllib2.URLError as e:
                if hasattr(e, 'code') and e.code == 404:
                    i +=1
                delay_time(1)
                proxy, proxyPool = getProxyFromPool()
                continue
            except Exception as e:
                print e
                proxy, proxyPool = getProxyFromPool()
                delay_time(1)
                continue

def main():
    runSpider()

if __name__ =='__main__':
    sys.exit(main())
