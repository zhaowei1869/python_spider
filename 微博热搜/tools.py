import http.client
import time
import requests


import random
import requests


# 获取有效代理
def get_valid_proxy(max_retries=7):
    # 完整的代理地址列表
    proxy_list = [
        {"http": "https://218.91.127.220:8089"},
        {"http": "https://47.113.224.182:9999"},
        {"http": "https://5.161.93.162"},
        {"http": "https://60.174.1.63:8089"},
        {"http": "https://114.103.80.183:8089"},
        {"http": "https://183.236.232.160:8080"},
        {"http": "https://49.70.89.186:8089"},
        {"http": "https://140.210.196.193:6969"},
        {"http": "https://51.159.66.223:80"},

        # 添加更多代理地址...
    ]

    for _ in range(max_retries):
        # 随机选择一个代理地址
        selected_proxy = random.choice(proxy_list)
        print("随机选择的代理地址:", selected_proxy)

        # 构建代理字典
        proxies = selected_proxy

        test_url = "https://httpbin.org/get"

        try:
            response = requests.get(test_url, proxies=proxies, timeout=20)

            # 检查响应状态码
            if response.status_code == 200:
                print(f"代理 {selected_proxy} 有效，IP 地址为:", response.json()["origin"])
                return selected_proxy  # 返回有效的代理地址，退出函数
            else:
                print(f"代理 {selected_proxy} 响应状态码:", response.status_code)
        except Exception as e:
            print(f"代理 {selected_proxy} 发生错误:", str(e))
            continue  # 出现错误，继续循环尝试下一个代理
    else:
        print("无法获取有效代理数据")
        return None
#############################################################################################################


# 多次尝试获取页面数据
def get_page_with_retry(url, cookies, headers, proxies):
    max_retries = 5  # 最大重试次数
    retry_wait_time = 6  # 重试等待时间，单位：秒

    retries = 0
    # 随机选择一个代理地址
    while retries < max_retries:
        try:
            # # 设置多个ip代理
            # 定义多个代理地址列表
            response = requests.get(url=url, cookies=cookies, headers=headers, proxies=proxies)
            # response = requests.get(url=url, cookies=cookies, headers=headers)
            response.raise_for_status()
            return response
        except (requests.RequestException, http.client.RemoteDisconnected) as e:
            print(f"连接异常，等待 {retry_wait_time} 秒后重试... (重试次数: {retries + 1})")
            time.sleep(retry_wait_time)
            retries += 1

    print(f"重试次数已达最大限制，无法获取数据")
    return None
#############################################################################################################
