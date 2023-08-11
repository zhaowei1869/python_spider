import random
import requests

def get_valid_proxy(max_retries=3):
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
                return selected_proxy
            else:
                print(f"代理 {selected_proxy} 响应状态码:", response.status_code)
        except Exception as e:
            print(f"代理 {selected_proxy} 发生错误:", str(e))
            continue  # 出现错误，继续循环尝试下一个代理
    else:
        print("无法获取有效代理数据")
        return None


# 使用函数获取有效代理
# valid_proxy = get_valid_proxy()
# if valid_proxy:
#     print("有效代理地址:", valid_proxy)
# else:
#     print("没有找到有效代理地址")
