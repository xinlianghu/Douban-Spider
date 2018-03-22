# -*- coding: utf-8 -*-
# coding=utf-8
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

host = 'localhost'
user = 'root'
password = 'admin'
database = 'test'

class InfoError(Exception):
    def __init__(self,value):
        self.value = value

class BasicInfo(object):
    def __init__(self,info ):
        self.id = 0
        self.name = ''
        self.director = ''
        self.country = ''
        self.tscore = '0'
        self.staring = ''
        self.language = ''
        self.type = ''
        self.alias = ''
        self.year = ''
        self.num = '0'
        self.tag = ''
        try:
            self.id = info['索引'].replace(' / ','/').strip()
            self.tag = info['类别'].replace(' / ','/').strip()
            self.name = info['名字'].replace(' / ','/').strip()
            self.director = info['导演'].replace(' / ','/').strip()
            self.country = info['制片国家/地区'].replace(' / ','/').strip()
            self.tscore = info['总评分'].replace(' / ','/').strip()
            self.staring = info['主演'].replace(' / ','/').strip()
            self.language = info['语言'].replace(' / ','/').strip()
            self.year = info['出品时间'].replace(' / ','/').strip()
            self.type = info['类型'].replace(' / ','/').strip()
            self.alias = info['又名'].replace(' / ','/').strip()
            self.num = info['评分人数'].replace(' / ','/').strip()
        except:
            pass
            #raise InfoError(e.message +'信息格式错误,无法正确解析')

    def __str__(self):
        info = ""
        info += "索引:%s\n" % self.id
        info += "名字:%s\n" % self.name
        info += "分类:%s\n" % self.tag
        info += "导演:%s\n" % self.director
        info += "主演:%s\n" % self.staring
        info += "总评分:%s分\n" % self.tscore
        info += "评分人数:%s\n" % self.num
        info += "制片国家/地区:%s\n" % self.country
        info += "语言:%s\n" % self.language
        info += "类型:%s\n" % self.type
        info += "出品时间:%s\n" % self.year
        info += "又名:%s\n" % self.alias
        return info

def init_database():
        conn = MySQLdb.connect(host,user,password,database,charset = 'utf8')
        cursor = conn.cursor()
        return conn,cursor

def create_table(db,cursor):
    CREATE = '''
    CREATE TABLE IF NOT EXISTS movie_info (
    id INT  NOT NULL AUTO_INCREMENT,
	name VARCHAR(256) NOT NULL,
	tag VARCHAR(10) NOT NULL,
	director VARCHAR(256) NOT NULL,
	country VARCHAR(256) NOT NULL,
	tscore VARCHAR(10) NOT NULL,
	num VARCHAR(20) NOT NULL,
	staring VARCHAR(512) NOT NULL,
	language VARCHAR(40) NOT NULL,
	year VARCHAR(20) NOT NULL,
	type VARCHAR(256) NOT NULL,
	alias VARCHAR(256) NOT NULL,
	PRIMARY KEY(id)
	) default charset=utf8;
    '''
    try:
        cursor.execute(CREATE)
        db.commit()
    except Exception as e:
        print e
        db.rollback()
def save(db,cursor,movieInfo):
    filed = movieInfo.__dict__
    keyList = filed.keys()
    key = ''
    for i in keyList:
        key += str(i) + ','
    key = key[:-1]
    value = ''
    valueList = filed.values()
    for i in valueList:
        if isinstance(i,str):
            value +=  '\"' + i + '\"' + ','
        else:
            value += str(i) + ','
    value = value[:-1]
    INSERT = "INSERT INTO movie_info ( %s ) VALUES( %s )" %(key,value)
    print INSERT
    try:
        cursor.execute(INSERT)
        db.commit()
        print "insert succes!"
    except Exception as e:
        print e
        db.rollback()



