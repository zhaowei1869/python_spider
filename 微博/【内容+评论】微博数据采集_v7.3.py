#encoding:utf-8
"""
python版本：3.6.8(64位)
编辑器：pycharm 2020.1.3
系统：windows 10 教育版 64位
"""
import requests # 请求库，模拟浏览器请求网站（服务器）
from bs4 import BeautifulSoup # HTML 文档解析器（用于筛选我们自己想要的内容）lxml 一定要安装。
import json # 解析字典数据（字符串字典数据转成字典数据，用key取值出来）
import csv # 把爬取的数据写入到CSV中,数据类型比如 list 才能写入
import pandas as pd # 是基于NumPy 的一种工具，该工具是为解决数据分析任务而创建的
import math # 模块提供了许多对浮点数的数学运算函数。
import time # 时间处理相关的库
import random # 随机
import datetime # # 时间处理相关的库
from datetime import date # # 时间处理相关的库

today_time = datetime.datetime.now().strftime('%Y-%m-%d') # 今日日期

class wbTool():

    # def __init__(self):
    #     pass

    def extractUid(self,url):
        """
        提取UID
        :return:
        """
        ids = str(url).split('/')[-1].split('?')[0]
        return ids

    def cleaningContent(self,text):
        """
        清洗微博内容文本数据
        :param text: 微博内容
        :return:
        """

        content = str(text).replace('\n','').replace(' ','').replace('\u200b','').replace('\ue627','')
        return content
    def textCleaning(self,text):
        """
        文本清洗，微博其他文本内容清洗
        :param text:
        :return:
        """
        text = str(text).replace('\n', '').replace(' ', '')
        return text

    def basicDataProcessing(self,text):
        """
        处理转发，评论，点赞数据
        :param text:
        :return:
        """
        text = str(text).replace('转发 ','0').replace(' 转发 ','0').replace('评论','0').replace(' \n','').replace(' ','0').replace('\n','').replace('赞','0').replace('转发','0')
        return text

    def weiboTime(self,timestr):

        timestr = str(timestr).split('转赞人数超过')[0]

        if '分' in timestr:
            division = timestr.split('分')[0]
            nowtime = int(time.time()) - int(division) * 60
            timeArray = time.localtime(nowtime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return otherStyleTime

        if '秒' in timestr:
            division = timestr.split('秒')[0]
            nowtime = int(time.time()) - int(division)
            timeArray = time.localtime(nowtime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return otherStyleTime

        if '今天' in timestr:
            otherStyleTime = today_time + ' ' + str(timestr).replace('今天', '') + ':00'  # # 发布时间
            return otherStyleTime

        if '月' in str(timestr) and '年' not in str(timestr):
            releaseTime = f'{date.today().year}年' + str(timestr) + ':00'  # # 发布时间
            otherStyleTime = releaseTime.replace('日', ' ').replace('年', '-').replace('月', '-')
            return otherStyleTime

        if '年' in str(timestr) and '月' in str(timestr) and '日' in str(timestr):
            otherStyleTime = timestr.replace('日', ' ').replace('年', '-').replace('月', '-')
            releaseTime = otherStyleTime + ':00'  # # 发布时间
            return releaseTime

    def saveCsv(self,filename, content):
        "保存数据为CSV文件 list 写入"
        fp = open(f'{filename}.csv', 'a+', newline='', encoding='utf-8-sig')
        csv_fp = csv.writer(fp)
        csv_fp.writerow(content)
        fp.close()
        print(f'正在写入:{content}')

    def get_time_ranges(self,from_time, to_time, frequency):
        """
        时间转换 2
        :param from_time:
        :param to_time:
        :param frequency:
        :return:
        """
        from_time, to_time, frequency = pd.to_datetime(from_time), pd.to_datetime(to_time), frequency * 60
        time_range = list(pd.date_range(from_time, to_time, freq=f'{frequency}s'))
        if to_time not in time_range:
            time_range.append(to_time)
        time_range = [item.strftime('%Y-%m-%d %H:%M:%S') for item in time_range]
        time_ranges = []
        for item in time_range:
            f_time = item
            t_time = (datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=frequency))
            if t_time >= to_time:
                t_time = to_time.strftime('%Y-%m-%d %H:%M:%S')
                time_ranges.append([f_time, t_time])
                break
            time_ranges.append([f_time, t_time.strftime('%Y-%m-%d %H:%M:%S')])
        return time_ranges

    def weiboTime_start(self,t):
        """
        时间转换
        :param t:
        :return:
        """
        searchTime = str(t).split(':')[0].split(' ')
        dateStr = searchTime[0]
        timeStr = int(searchTime[-1])
        stime = f"{dateStr}-{timeStr}"

        return stime


class weibo_spider(wbTool):

    def __init__(self,url):

        self.url = url

    def getContent(self):
        """
        请求微博网站
        :return:
        """
        response = requests.get(self.url, headers=WEIBOCONTENT_HEADERS)  # 带上请求头模拟浏览器 请求微博内容
        if '未找到' in response.text:
            print('抱歉，未找到相关结果。')

            return None

        else:
            return response.content

    def analysisContent(self):
        """
        解析 清洗微博内容数据
        :return:
        """
        content = self.getContent() # 请求返回的数据
        if content != None:

            html = BeautifulSoup(content,'lxml')# 用BeautifulSoup 解析HTML文档。lxml库 相当于 BeautifulSoup 的芯片。
            HomePageContent = html.find('div', id="pl_feedlist_index")  # 整个内容在这个标签属性中
            try:
                weiboContent = HomePageContent.find_all('div', class_="card-wrap")  # 每个微博内容
            except:
                print('COOKIE异常,请停止程序,请刷新微博网站,重新登录之后获取COOKIE填入代码中,在重新运行程序!!!')
                print(f'当前获取开始时间是：{statrTime}')
                print(f'当前获取结束时间是：{endTime}')
                print('请修改时间,为当前已获取的时间，避免重复写入数据')
                time.sleep(60)

            else:
                for wc in weiboContent:
                    # print(wc)
                    if 'mid' in str(wc): # 排除热门文章-非搜索文章
                        nickname = wc.find('a',class_="name").text # 微博发布者昵称
                        avator = wc.find('div',class_="avator")
                        homeLink = "https:"+avator.find('a')['href'] # 个人主页链接
                        uid = self.extractUid(homeLink) # UID
                        mid = wc['mid'] # MID-->微博内容ID
                        txt = wc.find_all('p',class_="txt")[-1].text # 获取微博内容
                        txt = self.cleaningContent(txt) # 清洗微博内容
                        comeFrom = wc.find('p',class_="from")
                        if comeFrom == None:
                            comeFrom = wc.find('div', class_="from")
                        a2 = comeFrom.find_all('a')
                        if len(a2) == 2: # 判断是否有其他信息
                            weiboDetailedLink = "https:"+comeFrom.find('a',target="_blank")['href'] # 微博详细链接
                            publishingDevice = comeFrom.find('a',rel="nofollow").text # 发布来源
                        else:
                            weiboDetailedLink = "https:" + comeFrom.find('a', target="_blank")['href']  # 微博详细链接
                            publishingDevice = "NULL" # 如果没有显示发布来源，就设置为NULL
                        releaseTime = comeFrom.find('a',target="_blank").text # 发布微博时间
                        releaseTime = self.textCleaning(releaseTime) # 发布微博时间
                        releaseTime = self.weiboTime(releaseTime) # 发布微博时间
                        basicData = wc.find('div',class_="card-act").find_all('li')
                        if len(basicData) == 3:
                            basicData = basicData
                        elif len(basicData) >= 4:
                            basicData = basicData[1:]
                        basicDatalist = [int(self.basicDataProcessing(bd.text)) for bd in basicData] # 转发数,评论数,点赞数

                        # UID,MID,发布时间，微博内容，微博链接，发布者昵称，发布来源，主页链接，转发数，评论数，点赞数
                        essentialInformation = [uid+'\t',mid+'\t',releaseTime,txt,weiboDetailedLink,nickname,publishingDevice,homeLink,] + basicDatalist
                        # 昵称、性别、粉丝数、关注数、所属地址(IP)、微博数、是否认证、头像下载链接、媒体类型、log10,认证类型
                        blogger = self.GetBloggerinfo(uid)
                        data = essentialInformation + blogger
                        self.saveCsv(FILENAMES,data)

                        if judge == 'y' or judge == 'Y': # 刚开始运行程序的时候，判断输入是否要爬去评论。
                            self.getComment(mid,uid,max_id=0)

                try:
                    pages = html.find('ul', class_="s-scroll").find_all('a')
                except:
                    pass
                else:
                    pages = len(pages)  # 获取搜索关键词信息有多少页，总页码数
                    try:
                        nextPage = html.find('a', class_="next")  # 筛选出下一页的跳转链接，也就是我们爬取的链接，标签 a 属性为 class_="next"
                        nextPageJudgment = str(nextPage['href']).split('=')[-1]  # 筛选出下一页的页码数
                        if int(nextPageJudgment) > int(pages):  # 如果下一页页码 大于 总 页码数，就停止爬取。
                            pass
                        else:  # 否则就继续爬取
                            print(f'正在获取第 {nextPageJudgment} 页')
                            nextPage = 'https://s.weibo.com' + nextPage['href']
                            # self.getWeibo_content(nextPage)
                            weibo_spider(nextPage).analysisContent()
                    except:
                        pass


    def GetBloggerinfo(self,uid):

        """
        请求博主基本信息
        :return:
        """
        url = f'https://weibo.com/ajax/profile/info?uid={uid}'

        try:
            response = requests.get(url, headers=ASYNCHRONOUS_HEADERS)  # 带上请求头模拟浏览器 请求微博内容
            jsondata = json.loads(response.text)
            # data = jsondata['data']
            # print(jsondata)
        except:

            data = ['', '', '', '', '',
                        '', '', '', '', '', '','']
            return data
        else:
            if jsondata['ok'] == 1 or jsondata['ok'] == '1':
                data = jsondata['data']
                user = data['user']
                screen_name = user['screen_name']  # 搜索名称(作者昵称)
                description = user['description']  # 个性签名
                followers_count = user['followers_count']  # 粉丝数
                friends_count = user['friends_count']  # 关注数
                location = user['location']  # IP所属地址
                statuses_count = user['statuses_count']  # 动态数(微博数量)
                verified = user['verified']  # 是否认证
                avatar_large = user['avatar_large']  # 头像
                gender = user['gender']  # 性别 m/f
                if gender == 'm':
                    gender = '男'
                else:
                    gender = '女'
                if int(followers_count) > 10000:
                    publicMedia = '公共媒体'
                    log10 = math.log10(int(followers_count))
                else:
                    publicMedia = 'nan'
                    log10 = 'nan'
                if str(verified) == 'True':
                    verified_type_ext = user['verified_type_ext']  # 认证V
                    verified_type = user['verified_type']  # 认证V
                    if int(verified_type_ext) == 1 and int(verified_type) == 0:
                        memberType = '微博个人认证(红V)'
                    elif int(verified_type) == 3:
                        memberType = '微博官方认证(蓝V)'
                    elif int(verified_type) == 0 and int(verified_type_ext) == 0:
                        memberType = '微博个人认证(黄V)'
                    else:
                        memberType = ''
                    # 昵称、性别、粉丝数、关注数、所属地址(IP)、微博数、是否认证、头像下载链接、媒体类型、log10,认证类型
                    data = [screen_name, gender, description, followers_count, friends_count,
                                location, statuses_count, verified, avatar_large, publicMedia, log10, memberType]
                    return data
                else:
                    memberType = '无认证'
                    # 昵称、性别、粉丝数、关注数、所属地址(IP)、微博数、是否认证、头像下载链接、媒体类型、log10,认证类型
                    data = [screen_name, gender, description, followers_count, friends_count,
                            location, statuses_count, verified, avatar_large, publicMedia, log10,memberType]
                    return data

            else:
                data = ['', '', '', '', '',
                        '', '', '', '', '', '', '']
                return data

    def getComment(self,mid,uid,max_id,page=0):
        """
        抓取评论 只有一级评论
        :return:
        """
        url = 'https://weibo.com/ajax/statuses/buildComments?'
        parameter = {

            'is_asc': '0',
            'is_reload': '1',
            'id': mid,
            'is_show_bulletin': '1',
            'is_mix': '0',
            'max_id': max_id, # 用于翻页。
            'count': '20',
            'uid': uid,
            'fetch_level': '0',

        }
        result = requests.get(url,params=parameter,headers=ASYNCHRONOUS_HEADERS)
        # print(result.text)
        jsondata = json.loads(result.text)
        # print(jsondata)
        if jsondata['ok'] == 1 or jsondata['ok'] == '1':
            data = jsondata['data']
            total_number = jsondata['total_number']
            print(f'一共有{total_number}评论')
            for d in data:
                created_at = d['created_at']  # 评论时间
                struct_time = time.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')  # 评论时间
                time_array = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 评论时间
                text_raw = d['text_raw'] # 评论内容
                user = d['user']
                comment_userid = user['id']
                screen_name = user['screen_name'] # 评论用户昵称
                description = user['description'] # 评论用户签名
                followers_count = user['followers_count'] # 关注数量
                friends_count = user['friends_count'] # 粉丝数量
                try:
                    like_counts = d['like_counts']  # 评论点赞数
                except:
                    like_counts = 0
                statuses_count = user['statuses_count'] # 作品数
                location = user['location'] # IP所属

                data = [mid+'\t',uid+'\t',time_array,text_raw,comment_userid,screen_name,description,followers_count,friends_count,like_counts,statuses_count,location]
                self.saveCsv(COMMENT_FILENAME,data)

            if data != []:
                max_id = jsondata['max_id']
                if max_id == 0 or max_id == '0':
                    pass
                else:
                    page += 1
                    page_count = total_number / 10
                    if page > page_count:
                        pass
                    else:
                        print(f'正在爬取第{page}页,评论数据中...')
                        t = random.randint(6,20)
                        print(f'休息{t}秒后继续爬取下页评论')
                        time.sleep(t)
                        self.getComment(mid, uid, max_id, page)
            else:
                print(jsondata['trendsText'])

if __name__ == '__main__':

    # 换上自己的COOKIE

    COOKIES = '_T_WM=86056691407; WEIBOCN_FROM=1110006030; SUB=_2A25JUh0oDeRhGeFM71EY8CvFyjSIHXVqvKNgrDV6PUJbktANLXD4kW1NQNoBZpnf8JgkmjRV6tWvkJTQL4gJ2Rw-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWxi-a8iPLUunIqPiBsD23D5NHD95QNeoB01K5f1K2RWs4DqcjM1K-c1CH8SE-4BE-4xbH8SC-ReC-RSNSLUJHE9Btt; SSOLoginState=1683385720; MLOGIN=1; __bid_n=187f19be8139ba3d244207; FPTOKEN=xyBtObLhGif3UcWcQVmdu4+OhPEFPWnE9ebtmZhypsOBR49gY0fXMY+4FkNHAHn8dZrx4oVCk+n/UrnR3kGSgamYp9jfh4JYlT61YwbbZUg/zyy3LybaobcN+ZNk5xlE60bAV3w5MhzEZWVnEVA0hv+ca8tD7cn96b+mR+MU6GnKnaH6+4jv8ZZymQdW/HPSxY12MwrDg7mk3Ihkz/PXiXJHPeK4DRs4f7qMpZdqaDUVhr7a7NL2JDf5ZXsjiX8exauu6fnyNcepOIrv+3IiVZtz98OQY6mjz9/l9g2GIdptgHtEi74tnFii6SUUvW/xWXQvVjXOQrC5j2w7cUWGgY24ipPfi/k3D6hUCkbGXboD3IqMxYHRg9s1Y0gAD7AXp8EnxAhWsWra4UjWN+85kA==|6gcdkj01IyhzV+6x89H4X6ni/XB0MNNPuyp2rTa7nLk=|10|a2617e0521b6b5ad1a5f620cdbff0d37; XSRF-TOKEN=a9b847; mweibo_short_token=76b612df38; M_WEIBOCN_PARAMS=oid=4898526297853254&luicode=20000174&lfid=4898525709601290'

    WEIBOCONTENT_HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 这里最重要的就是COOKIE，需要登录后爬取，不用担心封号。
        'cookie': COOKIES,
        # USER-Agent 是伪装自己是可视化浏览器，非机器人。
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }

    ASYNCHRONOUS_HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-version': 'v2.40.12',
        'cookie': COOKIES,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',

    }

    from_time = '2023-01-01 00:00:00'  # 爬取的开始时间
    to_time = '2023-3-31 23:59:59'  # 爬取的结束时间
    frequency = 60 * 6  # 分钟 爬取间隔时间 1天 24*60=
    """
    间隔时间：
        微博有限制50页，1月1日-2日的微博数据，1日00：00-02：00 ==50页，2-4点，也有50页，4-6点也有。00：00-23：59分。
        12个2小时，12*50页 = 600页。
    """
    keyword = ['日本核污水']  # 关键词

    print(keyword)

    FILENAME = "_".join(keyword)

    # 文件名称
    FILENAMES = f'{FILENAME}2023.02.01-2023.03.31'

    # 评论文件名称
    COMMENT_FILENAME = f'{FILENAME}评论2023.02.01-2023.03.31'


    col = ['UID', 'MID', '发布时间', '微博内容', '微博链接', '发布者昵称', '发布来源', '主页链接', '转发数', '评论数', '点赞数', '博主昵称', '性别', '个人签名',
           '粉丝数', '关注数', '所属IP地址', '微博数',
           '是否认证', '头像链接', '媒体类型', 'log10', '认证类型']

    wbTool().saveCsv(FILENAMES, col)
    # print('程序准备开始运行')

    comment_col = ['MID', 'UID', '评论时间', '评论内容', '评论人UID', '评论人昵称', '评论人个性签名', '关注数量', '粉丝数量', '点赞数量', '作品数', 'IP所属']

    wbTool().saveCsv(COMMENT_FILENAME, comment_col)

    remind = """
       请回答是否要抓取评论数据，如果要抓评论内容，请输入y。
       提醒评论数据是单独的文件，并没有与微博内容文件合并，抓完数据需要用MID字段自行匹配对应微博。
        
        1、评论数据并不是显示多少就能抓取多少，例如一共6条评论只抓取3条的原因: 
            1) 微博主动屏蔽了非法关键词;
            2) 一级评论是有3条，其他3条可能是二级评论或者三级评论;
            3) 微博限制显示条数;
        2、评论只抓取一级评论。如需要二级评论需要自己修改代码。
        3、自己修改代码时，发生报错，店长概不负责。除非额外费用，可以请求店长帮忙协助。
        4、直接运行报错请检查是否填入COOKIE。requests,bs4,lxml包是否安装。
       """

    print(remind)
    # judge = input('是否要抓取评论数据[y/n]：')
    judge = 'y'
    Sleeptime_count = 0
    k = wbTool().get_time_ranges(from_time, to_time, frequency)
    for x in k:
        print(f'\n正在爬取时间段为:{str(x[0])}~{str(x[-1])}')
        statrTime =  wbTool().weiboTime_start(str(x[0]))
        endTime =  wbTool().weiboTime_start(str(x[-1]))
        Sleeptime_count += 1
        '随机延迟，尝试反爬取'
        if Sleeptime_count % 6 == 0:
            print('\n短暂休息一下 随机休息5--20秒\n')
            time.sleep(random.randint(5,20))

        print(f'\n正在爬取关键词为:{keyword}的数据')
        url = f'https://s.weibo.com/weibo?q={keyword}&typeall=1&suball=1&timescope=custom:{statrTime}:{endTime}&Refer=g'
        weibo_spider(url).analysisContent()





