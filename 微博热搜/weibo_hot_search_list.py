import json
import random
import sys
import time
from datetime import datetime
from urllib import parse
import redis
import os


sys.path.append(r"E:\代码学习\python_spider\A工具函数")
from tools import get_valid_proxy, get_page_with_retry

# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

# 获取热搜榜详情页数据  ###################################################################################################
def get_hot_search_page(proxies, cookies, headers):

    url_hot_search_list = f'https://weibo.com/ajax/side/hotSearch'  # 微博热搜榜
    # url_info = f"https://s.weibo.com/weibo?q=%23{parse.quote(name)}%23"  # 微博热搜榜详情页
    # https://s.weibo.com/weibo?q=%23%E8%87%B4%E6%95%AC%E9%97%BB%E6%B1%9B%E8%80%8C%E5%8A%A8%E7%9A%84%E4%BD%A0%23
    print('\n', '热搜榜请求数据页面：', url_hot_search_list)

    try:
        response = get_page_with_retry(url_hot_search_list, cookies, headers, proxies)

        if response.json().get('data') and response.status_code == 200:
            realtime_list = response.json()['data']['realtime']

            with open(f'weibo_hot_search_data.csv', 'a', encoding='utf-8') as f:
                f.write(f'{current_time}  微博热搜榜\n\n')
                f.write(f'排名,微博内容,类别,微博id,热度\n')

            '''# 创建文件夹（如果不存在）
            folder_path = f'./data/{current_day}'
            os.makedirs(folder_path, exist_ok=True)'''

            with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
                file.write(f'#### {current_time}  微博热搜榜\n\n')   # file.write('## 二级标题\n\n')
                # file.write(f'排名,微博内容,类别,微博链接,微博id,热度,raw_hot\n')
                # file.write(f'| 排名 | 微博内容 | 类别 | 微博链接 | 微博id | 热度 | raw_hot |\n')
                file.write('| 排名 | 微博内容 | 类别 |\n')
                file.write('| --- | --- | --- |\n')

            key = current_time + '_rank'  # 键名
            r.hset('weibo_hot_search:key', key, key)

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

                print('热搜榜：', rank, note, category, url_info, mid, num, raw_hot)  # 打印热搜榜信息
                # 排名 微博内容 类别 微博链接 微博id 热度 raw_hot

                # 写入csv文件
                with open(f'weibo_hot_search_data.csv', 'a', encoding='utf-8') as f:
                    f.write(f'{rank},{note},{category},{url_info},{mid},{num},{raw_hot}\n')

                # with open('weibo_hot_search_data.md', 'a', encoding='utf-8') as file:
                #     file.write(f'{rank},{note},{category},{url_info},{mid},{num},{raw_hot}\n')
                with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
                    # file.write(f'| {rank} | {note} | {category} | {url_info} | {mid} | {num} | {raw_hot} |\n')
                    # 将微博链接作为超链接写入文件
                    # file.write(f'| 排名 | {rank} | [{note}]({url_info}) | {category} | {mid} | {num} | {raw_hot} |\n')
                    file.write(f'| {rank+1} | [{note}]({url_info}) | {category} |\n')

                # 写入Redis
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
                # key = current_time + '_rank'  # 键名
                # r.hset('weibo_hot_search:key', key, str(rank))
                r.hsetnx('weibo_hot_search:list', idkey, json_data)  # 使用hsetnx不覆盖已存在字段

        f.close()
        file.close()

    except Exception as e:
        print("An error occurred:", e)
    print('\n')
########################################################################################################################


# 获取话题榜详情页数据  ###################################################################################################
def get_topic_band(proxies, cookies, headers):
    # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    # r_topic_band = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

    # current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 当前时间
    with open(f'weibo_topic_band_data.csv', 'a', encoding='utf-8') as f:
        f.write(f'当前时间:{current_time}\n')
        f.write(f'排名,话题,导语,类别,话题链接,话题主持人,阅读,讨论,微博id\n')

    with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
        file.write(f'#### {current_time}  微博话题榜\n\n')  # file.write('## 二级标题\n\n')
        # file.write(f'排名,微博内容,类别,微博链接,微博id,热度,raw_hot\n')
        # file.write(f'| 排名 | 微博内容 | 类别 | 微博链接 | 微博id | 热度 | raw_hot |\n')
        file.write('| 排名 | 微博话题 | 类别 |\n')
        file.write('| --- | --- | --- |\n')

    key = current_time + '_rank'  # 键名
    r.hset('weibo_topic_band:key', key, key)

    for page in range(1, 11):
        url_topic_band = f'https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page={page}&count=10'
        try:
            response = get_page_with_retry(url_topic_band, cookies, headers, proxies)

            if response.json().get('data') and response.status_code == 200:
                statuses = response.json()['data']['statuses']
                for status in statuses:
                    # print(topic_band)
                    try:
                        rank = status['rank']  # .replace(',', '')  # 排名
                    except:
                        rank = 'None'

                    try:
                        topic = status['topic']  # 话题
                    except:
                        topic = 'None'

                    try:
                        summary = status['summary'].replace('\n', '').replace('\r', '').replace('\t', '').replace(',', '。')  # 导语
                    except:
                        summary = 'None'

                    try:
                        category = status['category']  # 类别
                    except:
                        category = 'None'

                    # url_info = f'https://s.weibo.com/weibo?q=%23{parse.quote(note)}%23'  # 微博链接
                    topic_url = f'https://s.weibo.com/weibo?q=%23{parse.quote(topic)}%23'

                    try:
                        claim = status['claim']  # 话题主持人
                    except:
                        claim = 'None'

                    try:
                        read = status['read']  # 阅读
                    except:
                        read = 'None'

                    try:
                        mention = status['mention']  # 讨论
                    except:
                        mention = 'None'

                    try:
                        mid = status['mid']  # 微博id
                    except:
                        mid = 'None'

                    print('话题榜：', rank, topic, summary, category, topic_url, claim, read, mention, mid)  # 打印话题榜信息
                    # 排名 话题 类别 话题链接 话题主持人 阅读 讨论 微博id

                    # 写入csv文件
                    with open(f'weibo_topic_band_data.csv', 'a', encoding='utf-8') as f:
                        f.write(f'{rank},{topic},{category},{topic_url},{claim},{read},{mention},{mid}\n')

                    with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
                        # file.write(f'| {rank} | {note} | {category} | {url_info} | {mid} | {num} | {raw_hot} |\n')
                        # 将微博链接作为超链接写入文件
                        # file.write(f'| 排名 | {rank} | [{note}]({url_info}) | {category} | {mid} | {num} | {raw_hot} |\n')
                        file.write(f'| {rank} | [{topic}]({topic_url}) | {category} |\n')

                    # 写入Redis
                    dict_hot_search = {
                        'rank': rank,
                        'topic': topic,
                        'summary': summary,
                        'category': category,
                        'topic_url': topic_url,
                        'claim': claim,
                        'read': read,
                        'mention': mention,
                        'mid': mid
                    }
                    dict_hot_search = {key: str(value) for key, value in dict_hot_search.items()}

                    # json_data = json.dumps(dict_hot_search)  # 将字典转换为JSON字符串并存储到Redis的同一个Hash表中   # 将字典转换为JSON字符串并编码为字节序列
                    json_data = json.dumps(dict_hot_search, ensure_ascii=False).encode('utf-8')

                    idkey = current_time + '_rank' + str(rank)  # 键名
                    # r.hset('weibo_hot_search_list:list', idkey, json_data)
                    r.hsetnx('weibo_topic_band:list', idkey, json_data)  # 使用hsetnx不覆盖已存在字段
            f.close()

        except Exception as e:
            print("An error occurred:", e)
        # t = random.randint(2, 5)
        # time.sleep(t)
    print('\n')
########################################################################################################################


# 获取要闻榜页面数据   ###################################################################################################
def get_news(proxies, cookies, headers):
    # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    # r_news = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

    url_news = f'https://weibo.com/ajax/statuses/news'
    try:
        response = get_page_with_retry(url_news, cookies, headers, proxies)

        # current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 当前时间
        with open(f'weibo_news_band_data.csv', 'a', encoding='utf-8') as f:
            f.write(f'当前时间:{current_time}\n')
            f.write(f'排名,话题,类别,话题链接,话题主持人,阅读,讨论\n')

        with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
            file.write(f'#### {current_time}  微博要闻榜\n\n')  # file.write('## 二级标题\n\n')
            # file.write(f'排名,微博内容,类别,微博链接,微博id,热度,raw_hot\n')
            # file.write(f'| 排名 | 微博内容 | 类别 | 微博链接 | 微博id | 热度 | raw_hot |\n')
            file.write('| 排名 | 微博要闻 | 类别 |\n')
            file.write('| --- | --- | --- |\n')

        key = current_time + '_rank'  # 键名
        r.hset('weibo_news:key', key, key)

        if response.json().get('data') and response.status_code == 200:
            band_list = response.json()['data']['band_list']
            for band in band_list:
                # print(topic_band)
                try:
                    rank = band['rank']  # .replace(',', '')  # 排名
                except:
                    rank = 'None'

                try:
                    topic = band['topic']  # 话题
                except:
                    topic = 'None'

                try:
                    # 导语 去除导语中的换行 summary = band['summary']
                    summary = band['summary'].replace('\n', '').replace('\r', '').replace('\t', '').replace(',', '。')
                except:
                    summary = 'None'

                try:
                    category = band['category']  # 类别
                except:
                    category = 'None'

                # url_info = f'https://s.weibo.com/weibo?q=%23{parse.quote(note)}%23'  # 微博链接
                news_url = f'https://s.weibo.com/weibo?q=%23{parse.quote(topic)}%23'

                try:
                    claim = band['claim']  # 话题主持人
                except:
                    claim = 'None'

                try:
                    read = band['read']  # 阅读
                except:
                    read = 'None'

                try:
                    mention = band['mention']  # 讨论
                except:
                    mention = 'None'

                # try:
                #     mid = band['mid']  # 微博id
                # except:
                #     mid = 'None'

                print('要闻榜：', rank, topic, summary, category, news_url, claim, read, mention)  # 打印话题榜信息
                # 排名 话题 类别 话题链接 话题主持人 阅读 讨论

                # 写入csv文件
                with open(f'weibo_news_band_data.csv', 'a', encoding='utf-8') as f:
                    f.write(f'{rank},{topic},{category},{news_url},{claim},{read},{mention}\n')

                with open(f'./data/{current_day}/weibo_hot_search{current_time}.md', 'a', encoding='utf-8') as file:
                    # file.write(f'| {rank} | {note} | {category} | {url_info} | {mid} | {num} | {raw_hot} |\n')
                    # 将微博链接作为超链接写入文件
                    # file.write(f'| 排名 | {rank} | [{note}]({url_info}) | {category} | {mid} | {num} | {raw_hot} |\n')
                    file.write(f'| {rank} | [{topic}]({news_url}) | {category} |\n')

                    # 写入Redis
                    dict_hot_search = {
                        'rank': rank,
                        'topic': topic,
                        'summary': summary,
                        'category': category,
                        'topic_url': news_url,
                        'claim': claim,
                        'read': read,
                        'mention': mention,
                        # 'mid': mid
                    }
                    dict_hot_search = {key: str(value) for key, value in dict_hot_search.items()}

                    # json_data = json.dumps(dict_hot_search)  # 将字典转换为JSON字符串并存储到Redis的同一个Hash表中   # 将字典转换为JSON字符串并编码为字节序列
                    json_data = json.dumps(dict_hot_search, ensure_ascii=False).encode('utf-8')

                    idkey = current_time + '_rank' + str(rank)  # 键名
                    # r.hset('weibo_hot_search_list:list', idkey, json_data)
                    r.hsetnx('weibo_news:list', idkey, json_data)  # 使用hsetnx不覆盖已存在字段
        f.close()

    except Exception as e:
        print("An error occurred:", e)
    print('\n')
########################################################################################################################


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
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")  # 当前时间  ("%Y-%m-%d_%H-%M-%S")
        current_day = datetime.now().strftime("%Y-%m-%d")  # 当前日期

        # 创建文件夹（如果不存在）
        folder_path = f'./data/{current_day}'
        os.makedirs(folder_path, exist_ok=True)

        get_hot_search_page(proxies, cookies, headers)
        get_topic_band(proxies, cookies, headers)
        get_news(proxies, cookies, headers)
        break
        '''print('等待6h后再次爬取')
        time.sleep(3600*6)  # 等待10秒后再次爬取  43200s=12h'''

    # while True:
    #     current_time = datetime.now()
    #     if current_time.minute == 0 and current_time.second == 0:  # 在整点时运行程序
    #         get_hot_search_list_page(proxies, cookies, headers)
    #
    #     time.sleep(1)  # 每隔1秒检查一次



