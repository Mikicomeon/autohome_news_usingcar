# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from lxml import etree
import re
import time
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()

headers = {
    'Accept': 'text/css,*/*;q=0.1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'x.autoimg.cn',
    'If-Modified-Since': 'Mon, 01 May 2017 02:56:38 GMT',
    'If-None-Match': '636292329983254104',
    'Referer': 'http://www.autohome.com.cn/use/1/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


def get_ThreadList(lastpage):
    page = lastpage
    for i in range(1,page+1):
        source_url = 'http://www.autohome.com.cn/use/' + str(i) + '/#liststart'
        print source_url
        time.sleep(2)
        res=requests.get(source_url)
        # req = res.text
        # wb_data = req.encode('gb2312')
        req = res.content
        selector = etree.HTML(req)
        host_url = source_url.split('/')[2]
        proxy_lists = selector.xpath('//div[@class="article-wrapper"]/ul[@class="article"]/li')
        for proxy_list in proxy_lists:
            news_url = title = publish_date = review_num = comment_num = tag = short_content  = comment_num =''

            objids = proxy_list.xpath('a/@href')
            if objids:
                objid = objids[0].split('/')[5].split('.')[0].split('-')[0]

                review_url = 'http://reply.autohome.com.cn/api/getData_ReplyCounts.ashx?appid=1&dateType=jsonp&objids=' + str(
                    objid)
                res1 = requests.get(review_url)
                if res1.status_code == 200:
                    req1 = res1.content
                    comment_nums = re.findall('replycountall":(.*?),', req1)
                    if comment_nums:
                        comment_num = comment_nums[0]

                news_urls = proxy_list.xpath('a/@href')
                if news_urls:
                    news_url = news_urls[0]

                titles = proxy_list.xpath('a/h3/text()')
                if titles:
                    title = titles[0].strip().replace('"','')

                tags = proxy_list.xpath('a/p/text()')
                if tags:
                    tag = (tags[0].split(']'))[0].replace('[','').split(' ')[-1]

                short_contents = proxy_list.xpath('a/p/text()')
                if short_contents:
                    if re.findall(']',short_contents[0]):
                        short_content = (short_contents[0].split(']'))[1].replace(' ','').replace('"','')
                    else:
                        short_content = short_contents[0].replace('"','')

                publish_dates = proxy_list.xpath('a/div[@class="article-bar"]/span[@class="fn-left"]/text()')
                if publish_dates:
                    publish_date_notjudge = publish_dates[0]
                    if re.findall(u'前',publish_date_notjudge):
                        time_now = int(time.time())    #####1493890478
                        # time_local = time.localtime(time_now)   ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
                        # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38

                        if re.findall(u'天',publish_date_notjudge):
                            cha1 = int(publish_date_notjudge.replace(u'天前',''))
                            cha1shijianchuo = 60*60*24*cha1
                            time_cha1 = time_now - cha1shijianchuo
                            time_cha1_local = time.localtime(time_cha1)
                            publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha1_local)

                        else:
                            cha2 = int(publish_date_notjudge.replace(u'小时前', ''))
                            cha2shijianchuo = 60*60*cha2
                            time_cha2 = time_now - cha2shijianchuo
                            time_cha2_local = time.localtime(time_cha2)
                            publish_date = time.strftime("%Y-%m-%d %H:%M:%S", time_cha2_local)

                    else:
                        publish_date = publish_date_notjudge


                review_nums = proxy_list.xpath('a/div[@class="article-bar"]/span[@class="fn-right"]/em[1]/text()')
                if review_nums:
                    review_num_wan = review_nums[0]
                    if re.findall(u'万',review_num_wan):
                        review_num = int(float(review_num_wan.replace(u'万',''))*10000)
                    else:
                        review_num = review_num_wan


                sql = ('INSERT IGNORE INTO `xcar_news_thread_20170503`'
                      '(`objid`,`news_url`,`title`,`publish_date`,`review_num`,`comment_num`,`tag`, `short_content`,`source_url`,`host_url`)'
                      'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                      ) % (
                          objid, news_url, title, publish_date, review_num, comment_num,tag,short_content,source_url,host_url)
                print sql
                mysql_dao.execute(sql)
            else:
                pass



if __name__ == '__main__':
    url = 'http://www.autohome.com.cn/use/1/#liststart'
    res = requests.get(url)
    req = res.content
    # req = res.text
    # wb_data = req.encode('gb2312')
    selector = etree.HTML(req)
    lastpages = selector.xpath('//div[@class="page"]/a[@target="_self"]/text()')
    lastpage = int(lastpages[-2])
    get_ThreadList(lastpage)
