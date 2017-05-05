# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import re
import time
import json
import pymysql
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()

def get_commentInfo(objid,base_news_url,title,lastpage):
    for i in range(1,lastpage+1):
        url = 'http://reply.autohome.com.cn/api/comments/show.json?count=50&page=' + str(i) + '&id=' + objid + '&appid=1&datatype=jsonp&order=0&replyid=0'
        print url
        res = requests.get(url)
        if res.status_code == 200:
            req = res.text
            wb_data = req.encode('utf-8')
            start_position = 1
            match2 = re.search(r']}',wb_data)
            end_position = match2.end()
            json_chuan = wb_data[start_position: end_position]
            json_chuanchuan = json.loads(json_chuan)
            comment_lists = json_chuanchuan['commentlist']
            for comment_list in comment_lists:
                reply_id = comment_list['ReplyId']
                reply_name = comment_list['RMemberName']
                reply_floor = comment_list['RFloor']
                reply_contents = comment_list['RContent']

                re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
                re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
                re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
                re_br = re.compile('<br\s*?/?>')  # 处理换行
                re_h = re.compile('</?\w+[^>]*>')  # HTML标签
                re_comment = re.compile('<!--[^>]*-->')  # HTML注释
                re_http = re.compile('http:[^>]*html')  # HTML注释
                s = re_cdata.sub('', reply_contents)  # 去掉CDATA
                s = re_script.sub('', s)  # 去掉SCRIPT
                s = re_style.sub('', s)  # 去掉style
                # s = re_br.sub('\n', s)  # 将br转换为换行
                s = re_br.sub('', s)  # 将br转换为空
                s = re_h.sub('', s)  # 去掉HTML 标签
                s = re_comment.sub('', s)  # 去掉HTML注释
                reply_content = re_http.sub('', s)



                reply_dates = comment_list['replydate']
                time_now = int(time.time())
                if re.findall(u'前', reply_dates):
                    if re.findall(u'天', reply_dates):
                        cha1 = int(reply_dates.replace(u'天前', ''))
                        cha1shijianchuo = 60 * 60 * 24 * cha1
                        time_cha1 = time_now - cha1shijianchuo
                        time_cha1_local = time.localtime(time_cha1)
                        publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha1_local)
                    elif re.findall(u'小时', reply_dates):
                        cha2 = int(reply_dates.replace(u'小时前', ''))
                        cha2shijianchuo = 60 * 60 * cha2
                        time_cha2 = time_now - cha2shijianchuo
                        time_cha2_local = time.localtime(time_cha2)
                        publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha2_local)
                    elif re.findall(u'分钟', reply_dates):
                        cha3 = int(reply_dates.replace(u'分钟前', ''))
                        cha3shijianchuo = 60 * cha3
                        time_cha3 = time_now - cha3shijianchuo
                        time_cha3_local = time.localtime(time_cha3)
                        publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha3_local)
                    else:
                        cha4 = int(reply_dates.replace(u'秒前', ''))
                        cha4shijianchuo = cha4
                        time_cha4 = time_now - cha4shijianchuo
                        time_cha4_local = time.localtime(time_cha4)
                        publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha4_local)

                    reply_date = publish_date
                else:
                    reply_date = reply_dates
                # print objid,reply_id,reply_name,reply_date,reply_floor,reply_content,base_news_url,title
                sql = ('INSERT IGNORE INTO `xcar_new_comment_20170505`'
                        '(`objid`,`reply_id`,`reply_name`,`reply_date`,`reply_floor`,`reply_content`,`base_news_url`,`title`)'
                        'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")'
                        ) % (
                       objid, reply_id, reply_name, reply_date, reply_floor, reply_content, base_news_url,title)
                print sql
                try:
                    mysql_dao.execute(sql)
                except:
                    print '----------------------------------'




if __name__ == "__main__":
    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,objid,url,title FROM xcar_news_post_20170504 WHERE status_comment=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    for (id,objid,url,title) in res:
        id = id
        objid = objid
        title = title
        base_news_url = url
        comment_url = 'http://reply.autohome.com.cn/api/comments/show.json?count=50&page=1&id=' + objid + '&appid=1&datatype=jsonp&order=0&replyid=0'
        res = requests.get(comment_url)
        if res.status_code == 200:
            wb_data = res.content
            wb_data_qunull = wb_data.replace('null', '0')
            req = eval(wb_data_qunull)
            comment_count = int(req['commentcountall'])
            if comment_count%50 != 0 :
                totalpage = comment_count/50+1
            else:
                totalpage = comment_count/50
            pagenum = totalpage
            if pagenum >= 2:
                lastpage = 2
            else:
                lastpage = pagenum
            try:
                get_commentInfo(objid,base_news_url,title,lastpage)
            except:
                print 'error'
            else:
                sql2 = 'UPDATE `xcar_news_post_20170504` SET `status_comment`="0" WHERE (`id`="%s")' % id
                print(sql2)
                mysql_dao.execute(sql2)


