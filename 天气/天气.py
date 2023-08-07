'''
[课题]: python 爬取历年天气数据并做可视化 - 学员实战项目

[时间]: 19：35

[老师]: 青灯教育 - 皑皑

[环境]: python 3.9 编译器：将代码翻译成 电脑能读懂的语言
 +
    pycharm 2021 编辑器： 用来写东西的软件

工具包 - 工具
[模块]: re, bs4, csv, requests, pandas, matplotlib
        -- win + R 输入cmd 打开命令窗口 输入安装命令 pip install 模块名
        pip install requests

先听一下歌 等一下后面进来的同学, 19:35正式开始讲课  [有什么喜欢听的歌曲 也可以在公屏发一下]
---------------------------------------------------------------------------------------------------

VIP试听课听课流程：
    1.  上课过程中，认真听讲，将项目逻辑弄通，将代码全部弄懂
    2.  不明白的地方在第几行，直接公屏提问行数
    3.  上课不要写代码，课后再自己试着写

听不懂？没关系
    扫右上角二维码添加铃铃老师，你可以领取：
    1.  今日项目源码一份
    2.  python基础教程 + 相关文档 一套

0 零基础

网页源代码

1. 获取网页源代码 - 通过页面地址 获取
2. 从网页源代码 中 提取需要的数据
3. 保存本地

'''
a = '_zap=2d25fc38-a2ac-4743-a1b2-cf8b21864216; d_c0=ALCY0JurvhWPTkgi7ZFAamRA9m3KfSAzMps=|1666352923; YD00517437729195%3AWM_TID=wCYWpJsVGk5BABBEUAaBNAEUX4eS4UE3; __snaker__id=Gac6pzcGmNjvFDi7; q_c1=de2402172d8041ca85bbfd2494c1d954|1666844575000|1666844575000; YD00517437729195%3AWM_NI=h5s8QsCaEcypB0eiy%2FMaM%2BqKM2Z6uqoNVjSLpjX%2FVz0aAnzyXYWqiRe0VrEND6nvm7rWUxtiSOwcxp0mBMcZ13ZS8KDKCF6YoeOv7T8YpP87qfQNpYN0r7gLVecaiosSWmo%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb8ea62a9a89f92f97fadb08bb2d15f839b9fb1c568989c89bad94e90f5a686cc2af0fea7c3b92aacebbdd9d47981bf8b84fc7c82f0ab8afc258fbf83ccf4418fee96d7f87bad929a8bd248b4b698d0d572f4bf8f8ff9739c879992ec5aa7f09a93c84688eaa297f03db2899b99f7639191b984fb7cf4b38eaee252f3ed96b4bb4188958da7b553adbb8197b660fc87c0b1bb3db3ba9faff3538ef0bed8e64896bbad82ec65b18d998eee37e2a3; z_c0=2|1:0|10:1687940298|4:z_c0|80:MS4xaV9HckRnQUFBQUFtQUFBQVlBSlZUWllZZzJVY2ZUc0lqbGJoelBlUTFDVmZyN1pQZ1Vic2RRPT0=|8521084564b6ba997fd379544d8aa77534bcb856d66a26ac0b6753db01735d35; _xsrf=151c4be8-452e-46a8-aa31-8d108836cae9; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1688533493,1688659505,1688664232,1688668931; KLBRSID=5430ad6ccb1a51f38ac194049bce5dfe|1689077922|1689077407; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1689089554'


# # 使用模块之前 先导入
# import requests
# from bs4 import BeautifulSoup
# import re
# import csv  # csv
#
# # 请求头 headers
# headers = {
#     # 浏览器的身份信息
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#
# }
# file = open('data.csv', mode='a', encoding='utf-8', newline='')
# csv_writer = csv.writer(file)
# csv_writer.writerow(
#     ['日期', '最高温', '最低温']
# )
#
# for year in range(2013, 2023):
#     for month in range(1, 13):
#         if month < 10:
#             month = f'0{month}'
#         date = f'{year}{month}'
#         # print(date)
#
#         # 1. 获取网页源代码 - 通过页面地址 获取
#         # 地址 链接 url
#         dizhi = f'https://lishi.tianqi.com/beijing/{date}.html'
#         # 通过地址获取数据
#         # 响应对象
#         # 对象： 身高 体重 。。。。
#         # text： 网页源代码
#         yuanma = requests.get(dizhi, headers=headers).text
#         # 反爬虫  -  反反爬虫
#         # print(yuanma)
#
#         # 2. 从网页源代码 中 提取需要的数据
#         #    1. 获取每天信息
#         # 'lxml': 解析规则
#         bs_duixiang = BeautifulSoup(yuanma, 'lxml')
#         li_data = bs_duixiang.find_all('li')
#         # print(li_data)
#
#         # 对于多个数据 如果要一个个的进行操作 for循环
#         for li_data_ in li_data:
#             # print(li_data_)
#             #    2. 从每天信息中 拿取 具体数据
#             # re: 正则模块
#             # 正则 ： 通过特殊规则 匹配字段
#             # .*: 任意的字段 任意的长度
#             riqi = re.findall('<div class="th200">(.*?) .*</div>', str(li_data_))
#             if riqi:
#                 qiwen = re.findall('<div class="th140">(.*)℃</div>', str(li_data_))
#                 print(riqi + qiwen)
#                 csv_writer.writerow(riqi + qiwen)


import pandas as pd
from matplotlib import pyplot as plt

# 1. 准备数据
data = pd.read_csv('data.csv', encoding='utf-8')

# 2. 创建空白图像
plt.figure(dpi=128, figsize=(20, 6))
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']

# 3. 画图
plt.plot(data['日期'], data['最高温'], color='red')
plt.plot(data['日期'], data['最低温'], color='cyan')
plt.fill_between(data['日期'], data['最高温'], data['最低温'], color='yellow')

# 4. 设置
plt.xticks(data['日期'][::300])
plt.title('北京')
plt.xlabel('日期')
plt.ylabel('气温')
plt.savefig('北京.jpg')


'''
从0开始学 - 就业 

课程体系 1. 直播课 + 录播回放（复习） + 解答辅导  - 解决你课上课后的问题  
        2. 重修  
        1. 不够认真
        2. 觉得自己没有掌握 
        
七个月 - 两年学习权限 
只要认真学 - 保证能学会  
15h 一周三节课 135/246 晚上 8-10 

VIP群 - 内推  -  外包 三四个月 

下个月开始支付学费 
腾讯课堂   助学活动  分期  12 18 24 
一个月 3-4百 

爬虫 数据分析 网站开发 
工作好找 薪资高  

人工智能 送我
自动化办公 送我 
Vue框架课程 送我
证书 

面试辅导  

几十号老师




 






'''










