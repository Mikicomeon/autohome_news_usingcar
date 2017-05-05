# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
import requests
from lxml import etree
import re
import time
import json
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()

# headers = {
#     'Accept': 'text/css,*/*;q=0.1',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Host': 'x.autoimg.cn',
#     'If-Modified-Since': 'Mon, 01 May 2017 02:56:38 GMT',
#     'If-None-Match': '636292329983254104',
#     'Referer': 'http://www.autohome.com.cn/use/1/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# }

def get_newsPostInfo(objid,url, lastpage,title,publish_date):
    title = title
    objid = objid
    publish_date = publish_date
    res4 = requests.get(url)
    req4 = res4.content
    selector4 = etree.HTML(req4)
    proxy_lists = selector4.xpath('//div[@class="column grid-14"]/div[@class="area article"]')
    for proxy_list in proxy_lists:
        source = type = editor = ''
        sources = proxy_list.xpath('div[@class="article-info"]/span[2]/a/text()')
        if sources:
            source = sources[0].strip()
        types = proxy_list.xpath('div[@class="article-info"]/span[3]/text()')
        if types:
            type = types[0].replace('类型：','')
        editors = proxy_list.xpath('div[@class="article-info"]/div[@class="editor-select-wrap"]/a/text()')
        if editors:
            editor = editors[0].strip()
        else:
            editors = proxy_list.xpath('//div[@class="article-info"]/div[@class="editor-select-wrap"]/div[@class="editor-select"]/div[@class="moreli-title"]/a/span/text()')
            if editors:
                editor = editors[0]
            else:
                editors = proxy_list.xpath(
                    '//div[@class="article-info"]/div[@class="editor-select-wrap"]/span/text()')
                if editors:
                    editor = editors[0]



    page = lastpage
    base_url = url.split('.html')[0]
    content = []
    for i in range(1, page + 1):
        target_url = base_url + '-' + str(i) + '.html'
        # print target_url
        res3 = requests.get(target_url)
        req3 = res3.content
        selector3 = etree.HTML(req3)

        contents = selector3.xpath('//div[@class="area article"]//div[@class="article-content"]/p/descendant::text()')
        f = lambda x: x.strip()
        contents_lists = [f(x) for x in contents]
        content_list = ''.join(contents_lists)
        content_page = content_list.replace('"', '')
        content.append(content_page)
    f1 = lambda x: x.strip()
    content1 = [f1(x) for x in content]
    content_true = ''.join(content1)
    # print objid,url,title,publish_date,source,type,editor,content_true
    sql = ('INSERT IGNORE INTO `xcar_news_post_20170504`'
           '(`objid`,`url`,`title`,`publish_date`,`source`,`type`,`editor`, `content_true`)'
           'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")'
           ) % (
        objid, url, title, publish_date, source, type, editor, content_true)
    print sql
    mysql_dao.execute(sql)





def get_specialNewsInfo(objid,title,url,publish_date):
    source = type = editor = ''
    objid = objid
    title = title
    res = requests.get(url)
    req = res.text
    wb_data = req.encode('utf-8')

    match1 = re.search(r'{"imgs":', wb_data)
    start_position = match1.start()
    match2 = re.search(r'}]}];', wb_data)
    end_position = match2.end()
    json_chuan = wb_data[start_position + 8: end_position - 3]
    # print type(json_chuan)
    json_chuanchuan = json.loads(json_chuan)
    content1 = []
    for aaa in json_chuanchuan:
        contents = aaa['Txt'].replace('&nbsp;', '').replace('<p>', '').replace('</p>', '').replace('<br />','').replace('</span>', '').replace('</a>', '').replace('<span class="hs_kw20_mainci">', '').replace('<span class="hs_kw21_mainci">', '').replace('<span class="hs_kw15_mainci">', '').replace('<span class="hs_kw0_mainci">', '').replace('<span class="hs_kw0_mainci">', '').replace('<a href="http://www.autohome.com.cn/user/201612/896703.html" target="_blank">','')
        content_null = contents.replace('<span class="hs_kw1_mainci">', '').replace('<span class="hs_kw11_mainci">','').replace('<span class="hs_kw10_mainci">', '').replace('<span class="hs_kw12_mainci">', '').replace('<span class="hs_kw14_mainci">', '').replace('<span class="hs_kw0_mainci">', '').replace('<span class="hs_kw14_mainci">', '').replace('<a href="http://www.autohome.com.cn/8768/0/1/conjunction.html" target="_blank">', '').replace('<span>','')

        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        re_http = re.compile('http:[^>]*html')  # HTML注释
        s = re_cdata.sub('', content_null)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        # s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_br.sub('', s)  # 将br转换为空
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        content = re_http.sub('', s)

        # print content
        content1.append(content)
    f = lambda x: x.strip()
    contents_lists = [f(x) for x in content1]
    content_list = ''.join(contents_lists)
    print content_list
    picture_if = "1"

    sql4 = ('INSERT IGNORE INTO `xcar_news_post_20170504`'
           '(`objid`,`url`,`title`,`publish_date`,`source`,`type`,`editor`, `content_true`,`picture_if`)'
           'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'
           ) % (
              objid, url, title, publish_date, source, type, editor, content_list,picture_if)
    print sql4
    mysql_dao.execute(sql4)


if __name__ == "__main__":
    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,objid,news_url,title,publish_date FROM xcar_news_thread_20170503 WHERE status=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    for (id,objid,news_url,title,publish_date) in res:
        id = id
        url = news_url
        title = title
        publish_date = publish_date
        res1 = requests.get(url)
        # print res1.status_code
        req = res1.content
        selector = etree.HTML(req)
        judge_if = selector.xpath('//div[@class="column grid-14"]/div[@class="area article"]')
        if judge_if:
            # print u'正常页面'
            nextpage_node = selector.xpath(
                '//div[@class="area article"]/div[@class="page"]/span[@class="page-item-info"]/text()')
            if nextpage_node:
                lastpage = int(nextpage_node[0].replace(u'共', '').replace(u'页', ''))
                try:
                    get_newsPostInfo(objid,url, lastpage,title,publish_date)
                except :
                    print "error"
                else:
                    sql3 = 'UPDATE `xcar_news_thread_20170503` SET `status`="0" WHERE (`id`="%s")' % id
                    print(sql3)
                    mysql_dao.execute(sql3)

            else:
                lastpage = 1
                try:
                    get_newsPostInfo(objid,url, lastpage,title,publish_date)
                except :
                    print "error"
                else:
                    sql1 = 'UPDATE `xcar_news_thread_20170503` SET `status`="0" WHERE (`id`="%s")' % id
                    print(sql1)
                    mysql_dao.execute(sql1)



        else:
            print u"图片新闻"
            # print url
            try:
                get_specialNewsInfo(objid,title,url,publish_date)
            except :
                print "error"
            else:
                sql2 = 'UPDATE `xcar_news_thread_20170503` SET `status`="0" WHERE (`id`="%s")' % id
                print(sql2)
                mysql_dao.execute(sql2)








