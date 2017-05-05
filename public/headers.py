# -*- coding: utf-8 -*-

import random
from config import Config


class Headers:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        # 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        # 'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        # 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        # 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
    ]
    referer = [
        'http://www.baidu.com/',
        'http://www.google.com.hk/',
        'http://www.so.com/',
        'http://www.google.com/',
        'http://www.sogou.com/',
        'http://www.youdao.com/'
    ]

    @staticmethod
    def get_headers():
        user_agent = random.choice(Headers.user_agent_list)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'hotels.ctrip.com',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) ',
            'User-Agent': user_agent,
            # 'Referer': random.choice(Headers.referer),
            # 'Referer': 'http://hotels.ctrip.com/',
            # 'Cookie' : '_bfa=1.1484037875047.xafss.1.1484045032173.1484730907315.4.5; _bfs=1.2; _bfi=p1%3D102086%26p2%3D102086%26v1%3D5%26v2%3D4; page_time=1484730911621%2C1484731992784; guid__=dc327570-d755-41bf-a5c0-88b1da2e50a4; MKT_Pagesource=PC; _jzqco=%7C%7C%7C%7C1484730912458%7C1.1742406217.1484730912296.1484730912296.1484731995296.1484730912296.1484731995296.0.0.0.2.2; __zpspc=9.1.1484730912.1484731995.2%234%7C%7C%7C%7C%7C%23; _ga=GA1.2.1355449604.1484730915',
            'X-Forwarded-For': '%s.%s.%s.%s' % (
                random.randint(50, 250), random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)),
            'CLIENT-IP': '%s.%s.%s.%s' % (
                random.randint(50, 250), random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
        }
        return headers
