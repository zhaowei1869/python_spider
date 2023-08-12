# 

#### 介绍
最近需要查看往年信息公告，但是不知道如何查找到，所以就想着写一个爬虫，爬取南信大信息公告网站的信息公告，方便查看。

#### 软件架构
软件架构说明


#### 安装教程

1.  导入Beautiful Soup库和requests库。没有这两个库自行安装

#### 使用说明

1.  vpn登录学校官网,进入学校信息公告页面（不登录无法查看具体内容，只可以爬取标题和链接）
2.  如需使用，将cookie替换成自己的cookie，将文件路径替换成自己的文件路径，运行即可。(第22行)
    页码如果有变化，自己修改一下页码即可。(第40行)![image-20230810101830933](https://cdn.jsdelivr.net/gh/zhaowei1869/learning_pictures/code/explain/image-20230810101830933.png)
3. requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

这个错误是由于网络连接被意外关闭而导致的。在使用 `requests.get` 发送请求时，连接可能在某种情况下被远程服务器关闭，导致无法得到服务器的响应。

有几种可能的原因和解决方法：

1)**网络问题**：你的网络连接可能不稳定，导致连接在传输数据时中断。你可以尝试检查你的网络连接，确保它稳定。

2)**服务器问题**：远程服务器可能出现问题，导致连接被关闭。这种情况下，你可能无法做太多事情，只能等待服务器恢复正常。

3)**请求频率过高**：如果你的脚本发送大量的请求，服务器可能会认为这是不正常的流量，从而关闭连接。你可以尝试降低请求频率，增加请求之间的间隔时间。

4)**使用错误的 URL**：确保你构建的 URL 是正确的，能够正确访问到目标网页。

5)**使用代理**：有时候，使用代理服务器可以帮助解决连接问题。

6)**异常处理**：你的代码中已经有一些异常处理，但可能需要进一步完善以处理这种情况。你可以考虑捕获 `ConnectionError` 异常，然后等待一段时间后重试。

示例代码：

```python
import time
import requests
from requests.exceptions import ConnectionError

# 其他代码...

def get_page(i):
    # 其他代码...
    
    try:
        response = requests.get(url=url, cookies=cookies, headers=headers)
        response.raise_for_status()
    except ConnectionError as ce:
        print('连接异常，等待重试...', ce)
        time.sleep(10)  # 等待一段时间后重试
        return  # 返回，不继续执行下面的代码
    
    # 其他代码...

# 其他代码...
```

请根据你的实际情况调整代码以适应可能的解决方案。

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  ~~使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md~~
2.  ~~Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)~~
3.  ~~你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目~~
4.  ~~[GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目~~
5.  ~~Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)~~
6.  ~~Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)~~
