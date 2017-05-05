# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import re
import time
import json
from lxml import etree
import pymysql
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()


def get_normalnews(objid,news_url,title,picture_if):
    res = requests.get(news_url)
    req = res.content
    selector = etree.HTML(req)
    picture_lists = selector.xpath(
        '//div[@class="area article"]/div[@class="article-content"]/p[@align="center"]/descendant::a[@target="_blank"]/img/@src')
    if picture_lists:
        for pictures in picture_lists:
            picture_link = pictures

            sql1 = ('INSERT IGNORE INTO `xcar_news_post_picture_20170505`'
                   '(`objid`,`news_url`,`title`,`picture_link`)'
                   'VALUES ("%s","%s","%s","%s")'
                   ) % (
                      objid, news_url, title, picture_link)
            print sql1
            mysql_dao.execute(sql1)




def get_picturenews(objid, news_url, title,picture_if):
    res = requests.get(news_url)
    req = res.text
    wb_data = req.encode('utf-8')
    match1 = re.search(r'{"imgs":', wb_data)
    start_position = match1.start()
    match2 = re.search(r'}]}];', wb_data)
    end_position = match2.end()
    json_chuan = wb_data[start_position + 8: end_position - 3]
    # print type(json_chuan)
    json_chuanchuan = json.loads(json_chuan)
    for pictures in json_chuanchuan:
        picture_link = pictures['smallimg']

        sql2 = ('INSERT IGNORE INTO `xcar_news_post_picture_20170505`'
               '(`objid`,`news_url`,`title`,`picture_link`)'
               'VALUES ("%s","%s","%s","%s")'
               ) % (
                  objid, news_url, title, picture_link)
        print sql2
        mysql_dao.execute(sql2)






if __name__ == "__main__":
    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,objid,url,title,picture_if FROM xcar_news_post_20170504 WHERE status_catch_picture=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    for (id,objid,url,title,picture_if) in res:
        print url
        id = id
        objid = objid
        title = title
        picture_if = picture_if
        news_url = url
        print picture_if

        if picture_if == '0':
            try:
                get_normalnews(objid,news_url,title,picture_if)
            except:
                print 'error'
            else:
                sql3 = 'UPDATE `xcar_news_post_20170504` SET `status_catch_picture`="0" WHERE (`id`="%s")' % id
                print(sql3)
                mysql_dao.execute(sql3)


        else:
            try:
                get_picturenews(objid, news_url, title,picture_if)
            except:
                print 'error'
            else:
                sql4 = 'UPDATE `xcar_news_post_20170504` SET `status_catch_picture`="0" WHERE (`id`="%s")' % id
                print(sql4)
                mysql_dao.execute(sql4)









