# coding=utf-8

"""
    1.爬取南信大官网信息公告：标题，发布时间，公告类别，发布单位，浏览量，公告详情链接等信息
    2.不需要登录，无法查看公告内容（若需查看公告内容，需要账号登录）
    3.南信大信息公告栏（不需登录）：https://bulletin.nuist.edu.cn/792/list1.htm
      南信大信息公告栏（需登录，课查看爬取公告详细内容）：url = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list1.htm'
    4.若是出错，需要将cookies，headers 替换成自己的cookies，headers
        (proxies代理不修改也可以)

    5.共获取14753条公告数据，获取数据较快，时间约3h
    获取数据如下：
        标题，发布时间，公告类别，发布单位，浏览量，公告详情链接
        正在爬取第1页
        中国气象局人事司致南京信息工程大学的感谢信,2023-08-10,党政事务,党委办公室、校长办公室、保密办公室（督查办公室）,295,https://client.vpn.nuist.edu.cn/2023/0810/c792a227087/page.htm,,
        关于召开2023年发展战略研讨会的预备通知,2023-07-08,会议通知,党委办公室、校长办公室、保密办公室（督查办公室）,2262,https://client.vpn.nuist.edu.cn/2023/0708/c792a226287/page.htm,,
        2023年暑假相关工作安排通知汇编,2023-06-28,其他,信息化建设与管理处、网络信息中心,9258,https://client.vpn.nuist.edu.cn/2023/0628/c792a225827/page.htm,,
        关于发布2023年暑假全校值班表的通知,2023-07-03,党政事务,党委办公室、校长办公室、保密办公室（督查办公室）,2526,https://client.vpn.nuist.edu.cn/2023/0703/c792a226095/page.htm,,
        关于开展2023年度江苏省科技创新协会科技创新奖评选活动的通知,2023-08-11,其他,科技产业处,75,https://client.vpn.nuist.edu.cn/2023/0809/c792a227072/page.htm,,
        关于做好第十二批南京市有突出贡献中青年专家选拔工作的通知,2023-08-11,组织人事,党委教师工作部、人事处、院士工作办公室、博士后管理中心,13,https://client.vpn.nuist.edu.cn/2023/0811/c792a227102/page.htm,,
        南京信息工程大学自助打印机经营服务项目中标候选人公示,2023-08-11,招标信息,招标办,71,https://client.vpn.nuist.edu.cn/2023/0811/c792a227101/page.htm,,
        金牛湖园区自动化实验室示波器等设备采购招标公告,2023-08-11,招标信息,招标办,49,https://client.vpn.nuist.edu.cn/2023/0811/c792a227099/page.htm,,
        关于编报2024年部门预算“一上”的通知,2023-08-11,其他,财务处,81,https://client.vpn.nuist.edu.cn/2023/0811/c792a227097/page.htm,,
        南京信息工程大学数学与统计学院藕舫论坛特邀美国匹兹堡大学王德华教授来我校作学术报告,2023-08-10,学术研讨,数学与统计学院（公共数学教学部）,62,https://client.vpn.nuist.edu.cn/2023/0810/c792a227091/page.htm,,
        中国气象局科技与气候变化司关于征集气候变化专题项目需求建议的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,60,https://client.vpn.nuist.edu.cn/2023/0810/c792a227088/page.htm,,
        关于组织申报2023年省级农业科技成果转化与集成推广项目的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,42,https://client.vpn.nuist.edu.cn/2023/0810/c792a227089/page.htm,,
        特邀湖南师范大学朱全新教授作学术报告,2023-08-10,学术报告,数学与统计学院（公共数学教学部）,97,https://client.vpn.nuist.edu.cn/2023/0809/c792a227083/page.htm,,
        关于举办“江苏省防灾减灾救灾救援（森林防灭火业务）专题培训班”的通知,2023-08-10,其他,继续教育学院,72,https://client.vpn.nuist.edu.cn/2023/0809/c792a227078/page.htm,,
        关于组织申报团簇构造、功能及多级演化重大研究计划2023年度项目的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,28,https://client.vpn.nuist.edu.cn/2023/0807/c792a227041/page.htm,,
        关于组织申报多物理场高效飞行科学基础与调控机理重大研究计划2023年度项目的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,27,https://client.vpn.nuist.edu.cn/2023/0809/c792a227080/page.htm,,
        关于组织申报集成芯片前沿技术科学基础重大研究计划2023年度项目的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,23,https://client.vpn.nuist.edu.cn/2023/0809/c792a227081/page.htm,,
        关于组织申报国家自然科学基金委员会化学科学部2023年度第二期专项项目（科技活动项目）的通知,2023-08-10,科研信息,科学技术处、国防军工科研处,20,https://client.vpn.nuist.edu.cn/2023/0809/c792a227082/page.htm,,
        南信大-盐都校地合作及产学研交流大会参会通知,2023-08-09,其他,科技产业处,199,https://client.vpn.nuist.edu.cn/2023/0809/c792a227073/page.htm,,
        关于暑假期间配送电系统检修停电的通知,2023-08-09,其他,总务处（后勤服务总公司）,131,https://client.vpn.nuist.edu.cn/2023/0808/c792a227065/page.htm,,
        科技企业技术需求信息发布（128-盐城盐都第三批次）,2023-08-09,其他,科技产业处,73,https://client.vpn.nuist.edu.cn/2023/0809/c792a227071/page.htm,,
        关于做好2023年创新型人才国际合作培养项目第二批人员申报工作的通知,2023-08-08,其他,研究生工作部、研究生院、学科建设处,146,https://client.vpn.nuist.edu.cn/2023/0807/c792a227036/page.htm,,
        关于组织申报西太平洋地球系统多圈层相互作用重大研究计划2023年度项目的通知,2023-08-08,科研信息,科学技术处、国防军工科研处,61,https://client.vpn.nuist.edu.cn/2023/0807/c792a227040/page.htm,,
        转发关于组织开展2023年江苏省大学生科普短视频创作大赛的通知,2023-08-07,其他,科学技术处、国防军工科研处,103,https://client.vpn.nuist.edu.cn/2023/0807/c792a227027/page.htm,,
        关于开展2023年度南京专利奖申报的通知,2023-08-07,其他,科技产业处,143,https://client.vpn.nuist.edu.cn/2023/0807/c792a227023/page.htm,,
        关于高性能碳纤维相关项目申报工作的通知,2023-08-07,科研信息,科学技术处、国防军工科研处,53,https://client.vpn.nuist.edu.cn/2023/0807/c792a227021/page.htm,,
        关于做好某单位配套规划第二批科研项目申报工作的通知,2023-08-07,科研信息,科学技术处、国防军工科研处,143,https://client.vpn.nuist.edu.cn/2023/0807/c792a227019/page.htm,,
        关于开展某单位基础加强计划技术领域基金项目申报工作的通知,2023-08-07,科研信息,科学技术处、国防军工科研处,139,https://client.vpn.nuist.edu.cn/2023/0807/c792a227016/page.htm,,
        2023年度江苏省本科优秀毕业论文（设计）与优秀团队拟推荐名单的公示,2023-08-07,教学考试,教务处（现代教育技术中心、藕舫学院）,506,https://client.vpn.nuist.edu.cn/2023/0807/c792a227017/page.htm,,
        2023届优秀本科毕业论文（设计）拟获奖名单公示,2023-08-06,教学考试,教务处（现代教育技术中心、藕舫学院）,680,https://client.vpn.nuist.edu.cn/2023/0806/c792a227012/page.htm,,
        关于组织2023级新生英语在线测试的通知,2023-08-06,教学考试,教务处（现代教育技术中心、藕舫学院）,256,https://client.vpn.nuist.edu.cn/2023/0806/c792a227007/page.htm,,
        关于组织2023级新生数学在线测试的通知,2023-08-06,教学考试,教务处（现代教育技术中心、藕舫学院）,244,https://client.vpn.nuist.edu.cn/2023/0806/c792a227006/page.htm,,
        大物名师讲座（第210期） ——特邀中国科学院大气物理研究所周敏强副研究员作报告,2023-08-06,学术报告,大气物理学院,254,https://client.vpn.nuist.edu.cn/2023/0806/c792a227005/page.htm,,
        2023年度省级生态环境科研项目（工程示范类）公开招标采购公告,2023-08-05,科研信息,科学技术处、国防军工科研处,67,https://client.vpn.nuist.edu.cn/2023/0805/c792a226985/page.htm,,
        关于做好国家留学基金委2024年“创新型人才国际合作培养项目”申报与年度总结工作的通知,2023-08-05,其他,研究生工作部、研究生院、学科建设处,70,https://client.vpn.nuist.edu.cn/2023/0805/c792a226983/page.htm,,
        特邀美国罗格斯大学纽瓦克分校郭锂教授作学术报告,2023-08-05,学术报告,数学与统计学院（公共数学教学部）,128,https://client.vpn.nuist.edu.cn/2023/0805/c792a226981/page.htm,,
        龙山遥测论坛（第二十六期）：特邀加拿大女王大学Dongmei Chen作学术报告,2023-08-04,学术报告,遥感与测绘工程学院,126,https://client.vpn.nuist.edu.cn/2023/0804/c792a226977/page.htm,,
        大物名师讲座（第209期）—特邀中国科学院上海光机所张龙研究员作报告,2023-08-04,学术报告,大气物理学院,212,https://client.vpn.nuist.edu.cn/2023/0804/c792a226966/page.htm,,
        关于做好2023年度国家社科基金冷门绝学研究专项申报组织工作的通知,2023-08-03,科研信息,社会科学处（校社科联、自贸区研究院）,109,https://client.vpn.nuist.edu.cn/2023/0803/c792a226961/page.htm,,
        关于北燃西区北换热站南侧、门诊楼东侧区域封闭施工的通知,2023-08-03,其他,总务处（后勤服务总公司）,91,https://client.vpn.nuist.edu.cn/2023/0803/c792a226958/page.htm,,
        国家国防科工局关于印发“十四五”技术基础科研计划第四批项目指南的通知,2023-08-03,科研信息,科学技术处、国防军工科研处,86,https://client.vpn.nuist.edu.cn/2023/0803/c792a226945/page.htm,,
        国防科工局“十四五”国防基础科研计划第四批项目申报的通知,2023-08-03,科研信息,科学技术处、国防军工科研处,76,https://client.vpn.nuist.edu.cn/2023/0803/c792a226944/page.htm,,
        南京信息工程大学消防设施设备消防维护保养项目中标结果公告,2023-08-02,招标信息,招标办,218,https://client.vpn.nuist.edu.cn/2023/0802/c792a226937/page.htm,,
        关于组织申报2022年度“江苏省社科应用研究精品工程优秀成果”的通知,2023-08-02,科研信息,社会科学处（校社科联、自贸区研究院）,142,https://client.vpn.nuist.edu.cn/2023/0802/c792a226924/page.htm,,
        关于征集化学科学部2024年度前沿导向重点项目/重点项目群立项建议的通知,2023-08-02,科研信息,科学技术处、国防军工科研处,58,https://client.vpn.nuist.edu.cn/2023/0802/c792a226923/page.htm,,
        关于征集2024年度化学科学领域重大项目立项建议的通知,2023-08-02,科研信息,科学技术处、国防军工科研处,51,https://client.vpn.nuist.edu.cn/2023/0802/c792a226922/page.htm,,
        关于组织申报国家自然科学基金“十四五”第三批重大项目的通知,2023-08-02,科研信息,科学技术处、国防军工科研处,150,https://client.vpn.nuist.edu.cn/2023/0802/c792a226921/page.htm,,
        关于揽江楼西北侧和文园12栋南侧区域封闭施工的通知,2023-08-02,其他,总务处（后勤服务总公司）,200,https://client.vpn.nuist.edu.cn/2023/0802/c792a226919/page.htm,,
        关于做好2023年度江苏省社科基金重大招标项目选题征集工作的通知,2023-08-02,科研信息,社会科学处（校社科联、自贸区研究院）,73,https://client.vpn.nuist.edu.cn/2023/0802/c792a226913/page.htm,,
        特邀美国加州大学（河滨分校）张旗教授来校作学术报告,2023-07-26,学术报告,数学与统计学院（公共数学教学部）,131,https://client.vpn.nuist.edu.cn/2023/0726/c792a226889/page.htm,,

"""

import datetime
import random
import time
from bs4 import BeautifulSoup
import requests
import http.client  # 导入 http 模块
from Obtain_valid_proxy import get_valid_proxy

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

MAX_RETRIES = 3  # 最大重试次数
RETRY_WAIT_TIME = 6  # 15  # 重试等待时间，单位：秒


# 请求页面，若第一次请求失败，则重试。最多重试 MAX_RETRIES 次
# 返回响应对象或 None
# 主要是该页面需要请求第二次才能获取到数据（第一次请求不到数据）
def get_page_with_retry(url, cookies, headers, proxies):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url=url, cookies=cookies, headers=headers, proxies=proxies)
            # response = requests.get(url=url, cookies=cookies, headers=headers)
            response.raise_for_status()
            return response  # 返回响应对象,退出函数
        except (requests.RequestException, http.client.RemoteDisconnected) as e:
            print(f"连接异常，等待 {RETRY_WAIT_TIME} 秒后重试... (重试次数: {retries + 1})")
            time.sleep(RETRY_WAIT_TIME)
            retries += 1

    print(f"重试次数已达最大限制，无法获取数据")
    return None


# 获取每一页的内容
def get_page(i):
    # proxies = proxies
    url = f'https://bulletin.nuist.edu.cn/792/list{i}.htm'
    # url = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list{i}.htm'
    # url2 = f'https://client.vpn.nuist.edu.cn/https/webvpn2ed9b9d0d8f4605e927e12405d4aac6bacb1d0129bab1534677e8c3ee143f76a/791/list{i}.psp'
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
        visit_count = news_item.find('span', class_='wp_listVisitCount').text.strip()

        """# 获取网页内容
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
"""

        print(title, date, leibie, organization, visit_count, href)

        # 内容p_tags保存到csv文件中,保存在一行中
        with open(f'data{current_time}.csv', 'a', encoding='utf-8') as f:
            f.write(title + ',' + date + ',' + leibie + ',' + organization + ',' + visit_count + ',' + href + ',' + ',' + '\n')
    print('保存成功！')
    f.close()


# 获取总页数
def get_total_page(cookies, headers, proxies):
    url = f'https://bulletin.nuist.edu.cn/792/list1.htm'
    print("函数：get_total_page", proxies)
    response = get_page_with_retry(url, cookies, headers, proxies)
    # print('response.text', response.text)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify() + '\n')
    # 找到class为"wp_articlecontent"的<div>标签，并提取其中的<p>标签的内容
    em_all_pages = soup.find('em', {'class': 'all_pages'}).text.strip()
    # 转换为int类型
    em_all_pages = int(em_all_pages)

    return em_all_pages


# for i in range(77, 299):  # 77
#     get_page(i)
#     # 随机休息6-10秒
#     t = random.randint(6, 10)
#     time.sleep(t)
#     print(f'休息{t}秒后，继续爬取第{i + 1}页', '\n')

if __name__ == '__main__':

    cookies = {
        '_gcl_au': '1.1.1025394217.1688718739',
        '_hjSessionUser_864760': 'eyJpZCI6IjhhZWQ2YzYwLWVlM2YtNTBlYy1iOTcxLTU4MTcwOTYyZTMzNyIsImNyZWF0ZWQiOjE2ODg3MTg3NDAyODMsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.3.589669986.1688718739',
        '_ga_4819PJ6HEN': 'GS1.1.1688718739.1.1.1688718812.0.0.0',
        '_ga_0HYE8YG0M6': 'GS1.1.1688718739.1.1.1688718812.0.0.0',
        'iPlanetDirectoryPro': 'pjMdIk3TNYqIZaBYILtcdsOrpD3pnUqL',
        'route': 'f52499b07f097dbe2b6d029348e465a0',
        'JSESSIONID': '0271C232CA8EA704D89F5E0BF20C38BC',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://bulletin.nuist.edu.cn/792/list.htm',
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

    # proxies = get_valid_proxy()
    all_pages = get_total_page(cookies, headers, get_valid_proxy())
    print('all_pages', all_pages, '\n')
    for i in range(1, all_pages + 1):  # 77   120  299
        print('获取代理 proxies')
        proxies = get_valid_proxy()
        get_page(i)
        # 随机休息6-10秒
        t = random.randint(6, 10)
        time.sleep(t)
        print(f'休息{t}秒后，继续爬取第{i + 1}页', '\n')
