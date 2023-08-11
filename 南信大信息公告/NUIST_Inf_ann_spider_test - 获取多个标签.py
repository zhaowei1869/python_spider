import datetime
import random
import time
from bs4 import BeautifulSoup
import requests
import http.client  # 导入 http 模块
from Obtain_valid_proxy import get_valid_proxy

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

MAX_RETRIES = 3  # 最大重试次数
RETRY_WAIT_TIME = 40  # 重试等待时间，单位：秒


def get_page_with_retry(url, cookies, headers, proxies):
    retries = 0

    # 随机选择一个代理地址

    while retries < MAX_RETRIES:
        try:
            # # 设置多个ip代理
            # 定义多个代理地址列表
            response = requests.get(url=url, cookies=cookies, headers=headers, proxies=proxies)
            # response = requests.get(url=url, cookies=cookies, headers=headers)
            response.raise_for_status()
            return response
        except (requests.RequestException, http.client.RemoteDisconnected) as e:
            print(f"连接异常，等待 {RETRY_WAIT_TIME} 秒后重试... (重试次数: {retries + 1})")
            time.sleep(RETRY_WAIT_TIME)
            retries += 1

    print(f"重试次数已达最大限制，无法获取数据")
    return None


# 获取每一页的内容
def get_page(i):
    # proxies = proxies
    url = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list{i}.htm'
    url2 = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list{i}.psp'
    print("正在爬取第" + str(i) + "页")
    with open(f'data{current_time}.csv', 'a', encoding='utf-8') as f:
        f.write("正在爬取第" + str(i) + "页" + '\n')  # 写入数据
    print("函数获取页面内容：proxies", proxies)
    response = get_page_with_retry(url, cookies, headers, proxies)

    """try:
        response = requests.get(url=url, cookies=cookies, headers=headers)
        print('response.status_code')
        # response.raise_for_status()  # 检查状态码，如果不是 200，将抛出 HTTPError 异常
    except requests.HTTPError as he:
        print('HTTPError 异常，等待重试...', he)
        time.sleep(60)  # 等待一段时间后重试
        return  # 返回，不继续执行下面的代码
    except ConnectionError as ce:
        print('连接异常，等待重试...', ce)
        time.sleep(60)  # 等待一段时间后重试
        return  # 返回，不继续执行下面的代码"""
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # span_tags = soup.find_all('span', {'class': 'btt'})
    # Find the parent container that holds all <li> elements
    parent_container = soup.find('ul', {'class': 'news_list clearfix'})

    # Find all <li> elements within the parent container
    news_items = parent_container.find_all('li', class_=lambda value: value and value.startswith('news n'))
    """
        当使用`find_all`方法查找HTML元素时，我们可以通过`class_`参数来指定要查找的元素的CSS类。在你的情况下，你希望查找所有具有以"news n"开头的类名的`<li>`元素。
    
        `class_`参数可以接受一个字符串、一个列表、一个函数或一个正则表达式来匹配CSS类。在这里，我们使用了一个lambda函数作为`class_`参数的值，该函数会对元素的CSS类进行判断。
    
        `value`是传递给lambda函数的参数，表示当前正在考虑的元素的CSS类值。通过 `value.startswith('news n')` 这个条件，我们判断元素的CSS类是否以 "news n" 开头。如果是的话，lambda函数返回 `True`，这样`find_all`方法就会将这个元素添加到结果列表中。
    
        这种方式使我们能够获取所有满足条件的`<li>`元素，而不用显式地指定每个可能的类名。这在需要批量处理不同类名的情况下非常方便。
    """

    # 提取每个条目的信息
    for news_item in news_items:
        # print('news_item', news_item)
        leibie = news_item.find('span', class_='wjj').find('a').get('title')
        title = news_item.find('span', class_='btt').find('a').get('title')
        href = 'https://client.vpn.nuist.edu.cn' + news_item.find('span', class_='btt').find('a').get('href')
        organization = news_item.find('span', class_='news_org').text.strip()
        date = news_item.find('span', class_='news_date').find('span', class_='arti_bs').text.strip()

        # 获取网页内容
        response = requests.get(href, cookies=cookies, headers=headers, proxies=proxies)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        # 找到class为"wp_articlecontent"的<div>标签，并提取其中的<p>标签的内容
        div_tag = soup.find('div', {'class': 'wp_articlecontent'})
        p_tags = div_tag.find_all('p')

        # 将多个<p>标签的文本内容连接在一起，并用换行隔开每个<p>标签的文本内容
        text = ''  # 初始化text为空字符串
        for p_tag in p_tags:  # 遍历所有<p>标签
            text += p_tag.text  # 将<p>标签的文本内容连接在一起

        print(title, date, leibie, organization, href, text)

        # 内容p_tags保存到csv文件中,保存在一行中
        with open(f'data{current_time}.csv', 'a', encoding='utf-8') as f:
            f.write(title + ',' + date + ',' + leibie + ',' + organization + ',' + href + ',' + text + ',' + '\n')

    print('保存成功！')

    f.close()


# 获取总页数
def get_total_page(cookies, headers, proxies):
    url = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list1.htm'
    print("函数：get_total_page", proxies)
    response = get_page_with_retry(url, cookies, headers, proxies)
    # print('response.text', response.text)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify() + '\n')
    # 找到class为"wp_articlecontent"的<div>标签，并提取其中的<p>标签的内容
    em_all_pages = soup.find('em', {'class': 'all_pages'}).text.strip()

    return em_all_pages


# for i in range(77, 299):  # 77
#     get_page(i)
#     # 随机休息6-10秒
#     t = random.randint(6, 10)
#     time.sleep(t)
#     print(f'休息{t}秒后，继续爬取第{i + 1}页', '\n')

if __name__ == '__main__':

    cookies = {
        'Hm_lvt_6e967eb120601ea41b9d312166416aa6': '1670370694,1670478582,1672845478',
        '_gcl_au': '1.1.1025394217.1688718739',
        '_hjSessionUser_864760': 'eyJpZCI6IjhhZWQ2YzYwLWVlM2YtNTBlYy1iOTcxLTU4MTcwOTYyZTMzNyIsImNyZWF0ZWQiOjE2ODg3MTg3NDAyODMsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.3.589669986.1688718739',
        '_ga_4819PJ6HEN': 'GS1.1.1688718739.1.1.1688718812.0.0.0',
        '_ga_0HYE8YG0M6': 'GS1.1.1688718739.1.1.1688718812.0.0.0',
        'GUESTSESSIONID': 'MWE3NmU5N2UtNjIwOS00YjRjLWEwMjktYmNjYjVjNTNhZTg2',
        'ENSSESSIONID': 'YmE5OTIyMGItNmE0MS00YjUxLWE3ODgtMjBiNWFhMzAyODQz',
        'iPlanetDirectoryPro': 'SI1RZwx59d7jhtajBGGX34ZhwlitPkoU',
        'clientInfo': 'eyJ1c2VybmFtZSI6IjIwMjIxMjI0MDA0MSIsInVzZXJJZCI6IjI3MTAyZmI0ODY4NjQ0NDNhMTIxNjc1MGIzOTk2Njk4IiwibG9naW5LZXkiOiI4Y0dLRnN1c1FEcG5NQURjIiwic2lkIjoiYmE5OTIyMGItNmE0MS00YjUxLWE3ODgtMjBiNWFhMzAyODQzIn0=',
        'vpn_timestamp': '1691727043',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'Hm_lvt_6e967eb120601ea41b9d312166416aa6=1670370694,1670478582,1672845478; _gcl_au=1.1.1025394217.1688718739; _hjSessionUser_864760=eyJpZCI6IjhhZWQ2YzYwLWVlM2YtNTBlYy1iOTcxLTU4MTcwOTYyZTMzNyIsImNyZWF0ZWQiOjE2ODg3MTg3NDAyODMsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.3.589669986.1688718739; _ga_4819PJ6HEN=GS1.1.1688718739.1.1.1688718812.0.0.0; _ga_0HYE8YG0M6=GS1.1.1688718739.1.1.1688718812.0.0.0; ENSSESSIONID=ZTdmZGFmMjQtMTc0OS00OTdkLWE5YjEtYmEwYzY0MDA4YmIx; iPlanetDirectoryPro=R0HipI3TUJKpoeRNLZZbqLM6N23VXMd3; clientInfo=eyJ1c2VybmFtZSI6IjIwMjIxMjI0MDA0MSIsInVzZXJJZCI6IjI3MTAyZmI0ODY4NjQ0NDNhMTIxNjc1MGIzOTk2Njk4IiwibG9naW5LZXkiOiJ4TGoySXFaTkgzb01tTXhqIiwic2lkIjoiZTdmZGFmMjQtMTc0OS00OTdkLWE5YjEtYmEwYzY0MDA4YmIxIn0=; GUESTSESSIONID=Nzg2MmY5OTYtODBkMC00MzMyLWExNDEtZmVkNDBiYTNlYWRj; vpn_timestamp=1691711076',
        'Referer': 'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list2.htm',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    proxies = get_valid_proxy()
    print("first Proxies", proxies)
    all_pages = get_total_page(cookies, headers, proxies)
    print('all_pages', all_pages)
    for i in range(115, 299):  # 77
        get_page(i)
        # 随机休息6-10秒
        t = random.randint(6, 10)
        time.sleep(t)
        print(f'休息{t}秒后，继续爬取第{i + 1}页', '\n')

