from datetime import datetime
import json
import time
from urllib import parse

import redis
import requests
import sys
sys.path.append(r"E:\代码学习\python_spider\A工具函数")
from tools import get_valid_proxy, get_page_with_retry


# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
'''r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)
'''
# 获取热搜榜页面数据
def get_hot_search_list_page(proxies, cookies, headers):
    url_hot_search_list = f'https://weibo.com/ajax/side/hotSearch'  # 微博热搜榜
    # url_info = f"https://s.weibo.com/weibo?q=%23{parse.quote(name)}%23"  # 微博热搜榜详情页
    # https://s.weibo.com/weibo?q=%23%E8%87%B4%E6%95%AC%E9%97%BB%E6%B1%9B%E8%80%8C%E5%8A%A8%E7%9A%84%E4%BD%A0%23
    print('\n', '热搜榜请求数据页面：', url_hot_search_list)

    response = get_page_with_retry(url_hot_search_list, cookies, headers, proxies)
    # print(response.json)
    # print(response.status_code)
    # print(response.json().get('data'))
    try:
        response = get_page_with_retry(url_hot_search_list, cookies, headers, proxies)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 当前时间
        with open(f'微博热搜/weibo_hot_search_list_data.csv', 'a', encoding='utf-8') as f:
            f.write(f'当前时间:{current_time}\n')
            f.write(f'排名,微博内容,类别,微博链接,微博id,热度,raw_hot\n')
        if response.json().get('data') and response.status_code == 200:
            realtime_list = response.json()['data']['realtime']
            # print('realtime_list', realtime_list)
            for realtime in realtime_list:
                # print(realtime)
                try:
                    rank = realtime['rank']  # 排名
                except:
                    rank = 'None'

                try:
                    category = realtime['category'].replace(',', '')  # 类别
                except:
                    category = 'None'

                try:
                    note = realtime['note']  # 微博内容
                except:
                    note = 'None'

                try:
                    mid = realtime['mid']  # 微博id
                except:
                    mid = 'None'

                url_info = f'https://s.weibo.com/weibo?q=%23{parse.quote(note)}%23'  # 微博链接

                try:
                    num = realtime['num']  # 热度
                except:
                    num = 'None'

                try:
                    raw_hot = realtime['raw_hot']  # 热度
                except:
                    raw_hot = 'None'

                print(rank, note, category, url_info, mid, num, raw_hot)  # 打印热搜榜信息
                # 排名 微博内容 类别 微博链接 微博id 热度 raw_hot

                # 写入csv文件
                with open(f'微博热搜/weibo_hot_search_list_data.csv', 'a', encoding='utf-8') as f:  # 微博热搜
                    f.write(f'{rank},{note},{category},{url_info},{mid},{num},{raw_hot}\n')

                '''# 写入Redis
                dict_hot_search = {
                    'rank': rank,
                    'note': note,
                    'category': category,
                    'url_info': url_info,
                    'mid': mid,
                    'num': num,
                    'raw_hot': raw_hot
                }
                dict_hot_search = {key: str(value) for key, value in dict_hot_search.items()}

                # json_data = json.dumps(dict_hot_search)  # 将字典转换为JSON字符串并存储到Redis的同一个Hash表中
                # 将字典转换为JSON字符串并编码为字节序列
                json_data = json.dumps(dict_hot_search, ensure_ascii=False).encode('utf-8')

                idkey = current_time + '_rank' + str(rank)  # 键名
                # r.hset('weibo_hot_search_list:list', idkey, json_data)
                r.hsetnx('weibo_hot_search_list:list', idkey, json_data)  # 使用hsetnx不覆盖已存在字段

                # r.hmset('weibo_hot_search_list:list', dict_hot_search)  # 每个热搜有独立的键
                # print(dict_hot_search)  # print(f"Data for rank {rank} stored in Redis.")'''

                """# # 写数据到Redis
                idkey = 'rank' + str(rank)  # 键名

                # hash表数据写入命令hmget，可以一次写入多个键值对
                # r.hmset(idkey, dict_hot_search)  # key是"foo" value是"bar" 将键值对存入redis缓存
                # r.hmset('weibo_hot_search_list', dict_hot_search)
                r.hset('weibo_hot_search_list', idkey, dict_hot_search)
                print(f"Data for rank {rank} stored in Redis.")"""
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    cookies = {
        'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5v9Ofp3gMZhWmJskW_p4bJ',
        'login_sid_t': 'fe3d7a7629bae85f24f94fb49bd3b0aa',
        'cross_origin_proto': 'SSL',
        'XSRF-TOKEN': 'SR7VcDx2QzJl2voXkoM_oojQ',
        'SUB': '_2AkMThKjPf8NxqwFRmPwXzWrmbIl0yQjEieKl2FkUJRMxHRl-yj9vqmootRB6OASGIIW9yxdO4_uFqBCxM4oj7BOszci6',
        '_s_tentry': 'passport.weibo.com',
        'Apache': '3717434107899.276.1691887614074',
        'SINAGLOBAL': '3717434107899.276.1691887614074',
        'ULV': '1691887614080:1:1:1:3717434107899.276.1691887614074:',
        'wb_view_log': '1494*9341.5',
        'WBPSESS': 'BP4XMQoD7Z31Vf3tBPaOodgFMCVmH3Tpk2UAkec7Na8ARQv2zvjGArjPV2p9fvVFFhE51SQzQMKX0QoRC42LZjP5dwX5OtZG0SwZaJG01p6EnTnC-8jHvp0nbNJz0FaSq2NLcn2E4u9tcz1yIT64iVNsfhW6bsSS9MjTMQvDtN0=',
    }

    # cookies = None

    headers = {
        'authority': 'weibo.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-version': 'v2.43.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5v9Ofp3gMZhWmJskW_p4bJ; login_sid_t=fe3d7a7629bae85f24f94fb49bd3b0aa; cross_origin_proto=SSL; XSRF-TOKEN=SR7VcDx2QzJl2voXkoM_oojQ; SUB=_2AkMThKjPf8NxqwFRmPwXzWrmbIl0yQjEieKl2FkUJRMxHRl-yj9vqmootRB6OASGIIW9yxdO4_uFqBCxM4oj7BOszci6; _s_tentry=passport.weibo.com; Apache=3717434107899.276.1691887614074; SINAGLOBAL=3717434107899.276.1691887614074; ULV=1691887614080:1:1:1:3717434107899.276.1691887614074:; wb_view_log=1494*9341.5; WBPSESS=BP4XMQoD7Z31Vf3tBPaOodgFMCVmH3Tpk2UAkec7Na8ARQv2zvjGArjPV2p9fvVFFhE51SQzQMKX0QoRC42LZjP5dwX5OtZG0SwZaJG01p6EnTnC-8jHvp0nbNJz0FaSq2NLcn2E4u9tcz1yIT64iVNsfhW6bsSS9MjTMQvDtN0=',
        'referer': 'https://weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2Fhot%2Fsearch',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'server-version': 'v2023.08.10.1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'SR7VcDx2QzJl2voXkoM_oojQ',
    }

    proxies = get_valid_proxy()
    while True:
        get_hot_search_list_page(proxies, cookies, headers)
        time.sleep(10)  # 等待10秒后再次爬取
    '''while True:
        current_time = datetime.now()
        if current_time.minute == 0 and current_time.second == 0:  # 在整点时运行程序
            get_hot_search_list_page(proxies, cookies, headers)

        time.sleep(1)  # 每隔1秒检查一次'''

