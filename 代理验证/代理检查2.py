import random
import requests

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
    # 'Cookie': 'Hm_lvt_6e967eb120601ea41b9d312166416aa6=1670370694,1670478582,1672845478; _gcl_au=1.1.1025394217.1688718739; _hjSessionUser_864760=eyJpZCI6IjhhZWQ2YzYwLWVlM2YtNTBlYy1iOTcxLTU4MTcwOTYyZTMzNyIsImNyZWF0ZWQiOjE2ODg3MTg3NDAyODMsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.3.589669986.1688718739; _ga_4819PJ6HEN=GS1.1.1688718739.1.1.1688718812.0.0.0; _ga_0HYE8YG0M6=GS1.1.1688718739.1.1.1688718812.0.0.0; GUESTSESSIONID=MWE3NmU5N2UtNjIwOS00YjRjLWEwMjktYmNjYjVjNTNhZTg2; ENSSESSIONID=YmE5OTIyMGItNmE0MS00YjUxLWE3ODgtMjBiNWFhMzAyODQz; iPlanetDirectoryPro=SI1RZwx59d7jhtajBGGX34ZhwlitPkoU; clientInfo=eyJ1c2VybmFtZSI6IjIwMjIxMjI0MDA0MSIsInVzZXJJZCI6IjI3MTAyZmI0ODY4NjQ0NDNhMTIxNjc1MGIzOTk2Njk4IiwibG9naW5LZXkiOiI4Y0dLRnN1c1FEcG5NQURjIiwic2lkIjoiYmE5OTIyMGItNmE0MS00YjUxLWE3ODgtMjBiNWFhMzAyODQzIn0=; vpn_timestamp=1691727043',
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


# 完整的代理地址列表
proxy_list = [
    {"http": "https://218.91.127.220:8089"},
    # {"https": "https://218.91.127.220:8089"},
    {"http": "https://47.113.224.182:9999"},
    # {"https": "https://47.113.224.182:9999"},
    {"http": "https://5.161.93.162"},
    # {"https": "https://5.161.93.162"},
    # 添加更多代理地址...
]

# 随机选择一个代理地址
selected_proxy = random.choice(proxy_list)
print("随机选择的代理地址:", selected_proxy)

# 构建代理字典
proxies = selected_proxy

test_url = "https://httpbin.org/get"
# test_url = "https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list1.htm"
try:
    print('proxies', proxies)
    response = requests.get(test_url, proxies=proxies)
    print('response.status_code', response.status_code)
    print(response.text)
    # 检查响应状态码
    if response.status_code == 200:
        print(f"代理 {selected_proxy} 有效，IP 地址为:", response.json()["origin"])
    else:
        print(f"代理 {selected_proxy} 响应状态码:", response.status_code)
except Exception as e:
    print(f"代理 {selected_proxy} 发生错误:", str(e))
