# -*- coding: utf-8 -*-

import time

class Config:
    #mysql配置
    mysql_host = "172.16.1.221"
    mysql_user = "chuanghe"
    mysql_password = 'chuanghe'
    mysql_dbname = "crawl_test"
    mysql_port = 3306
    mysql_charset = 'utf8'
    # mysql重试次数
    mysql_retry_times = 5
    # mysql 连接池 最大 连接数
    mysql_max_cached = 2

    #redis配置
    redis_host = "106.75.130.246"
    redis_auth = 'alb123'
    redis_retry_times = '5'
    # 爬虫线程数量
    clawler_num = 8
    # 休息时间
    sleep_time = 3600
    # 头信息
    headers_referer = 'https://sh.nuomi.com/'

    dir_path = '/mnt/crawler/weixin/'
    headers_path = '/mnt/crawler/weixin/'

    created_at = time.strftime('%Y-%m-%d %H:%M:%S')

    ruokuai_type = '2040'
    ruokuai_name = 'ricksun'
    ruokuai_pswd = 'ricksun123'
    ruokuai_soft_id = '72664'
    ruokuai_soft_key = 'e55265c2a42643f5a5ec562da8a10673'
