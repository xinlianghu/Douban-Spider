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
reload(sys)
sys.setdefaultencoding('utf-8')
req_headers = {
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
            }

def get(proxy,url):
    url = url
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)
    request = urllib2.Request(url, headers=req_headers)
    response = None
    try:
        response = opener.open(request)
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
    name = soup.find('span',  property="v:itemreviewed").text
    movieInfo['名字'] = str(name)

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
def runSpider(start,end,size = 10):
    db,cursor = init_database()
    create_table(db,cursor)
    url = "https://movie.douban.com/subject/"
    items = 0
    count = start-1
    counter = 0
    proxy = selectProxy()
    #proxy = {'https':'222.73.68.144:8090'}
    print 'select proxy:', proxy
    old_proxy = proxy
    index = start
    while index <= end:
        tempUrl = url + str(index)
        movieinfo = None
        if counter >= 1000:
            counter = 0
            while old_proxy == proxy:
                proxy = selectProxy()
            old_proxy = proxy
            print 'select proxy:',proxy
        html ,errorcode,reason= get(proxy,tempUrl)

        counter +=1
        if str(errorcode) == '302':
            db.close()
            print 'get the last html index:%d'%index
            return
        if html == None:
            print 'Get HTML from %s failed! ' % tempUrl,'Error code:',errorcode,'reason:',reason
            if errorcode == None:
                proxy = selectProxy()
                print 'select proxy:', proxy
            continue
        print 'Get HTML from %s success!'% tempUrl
        try:
            movieinfo = getMovieInfo(html)
            movieinfo['index'] = index
            print BasicInfo(movieinfo)
            save(db,cursor,BasicInfo(movieinfo))
            index +=1
        except Exception as e:
            print e
            continue
    db.close()

def getproxy():
    url = 'http://www.xicidaili.com/wn'
    header = req_headers
    header['Host'] ='www.xicidaili.com'
    request = urllib2.Request(url ,headers=header)
    response = urllib2.urlopen(request)
    html = response.read()
    if response.headers['Content-Encoding'] == 'gzip':
        html = zlib.decompress(html,16+zlib.MAX_WBITS)
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table',id="ip_list").find_all('tr')
    num = len(trs)
    proxy = []
    for i in range(1,num):
        tds = trs[i].find_all('td')
        if str(tds[4].get_text()) == '高匿':
            proxy.append({str(tds[5].get_text()).lower():str(tds[1].get_text()+':'+tds[2].get_text())})
    return proxy

def selectProxy():
    proxy = getproxy()
    num = len(proxy)
    index = int(random.uniform(0,num))
    return proxy[index]

def printInfo(movieinfo):
    for key in movieinfo.keys():
        print key,movieinfo[key]
runSpider(1295096,1295096+10000)
#html ,s,t= get("https://movie.douban.com/subject/1309046")
#movieinfo = getMovieInfo(html)
#getproxy()
