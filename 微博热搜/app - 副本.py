from flask import Flask, render_template
import redis
import json
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)


# Define a custom Jinja2 filter to flatten a list of lists
@app.template_filter('flatten')
def flatten_filter(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


# 连接到Redis服务器
redis_host = 'localhost'  # Redis服务器地址
redis_port = 6379  # Redis端口号
redis_db = 1  # 数据库索引

# 创建Redis连接对象
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)


@app.route('/')
def index():
    # 获取所有主键
    all_keys = r.hkeys('weibo_hot_search:key')

    # 为展示数据准备列表
    data_lists = []

    # 倒序遍历每个键并输出
    for key in reversed(all_keys):

    # 遍历主键并提取对应数据
    # for key in all_keys:
        data_list = []
        key_str = key.decode('utf-8')
        print(key_str)

        for i in range(0, 50):
            # 获取对应数据
            print(key_str + str(i))
            data = r.hget('weibo_hot_search:list', key_str + str(i))

            if data:
                data_dict = json.loads(data.decode('utf-8'))  # 将值转换为 JSON 对象
                print(data_dict)
                # data_list.append({"key": key_str + str(i), "data_dict": data_dict})  # 将键名和JSON数据添加到列表
                data_list.append({"key": key_str + str(i), "data_dict": data_dict})
            else:
                print(f"Data not found for key: {key_str + str(i)}")
        print(data_list)
        data_lists.append(data_list)
        print()
    # return render_template(f'index.html')
    print('data_lists', data_lists)
    print(len(data_lists))
    # json_data = json.dumps(data_list)  # Convert the list to JSON format
    # return render_template(f'index2.html', json_data=json_data)
    '''return render_template(f'index.html', data_lists=data_lists)'''

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    total = len(data_lists)
    pagination_data = data_lists[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('index_副本.html', data_lists=pagination_data, pagination=pagination)


if __name__ == '__main__':
    app.run(debug=True)
