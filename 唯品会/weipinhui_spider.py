import csv
import math
import random
import sys
import time

"""
    批量替换 Ctrl + R
        (.*?):(.*)
        '$1':'$2',
    
    
    批量删除 Ctrl + D
    批量复制 Ctrl + C
    批量粘贴 Ctrl + V
    批量注释 Ctrl + /
    批量取消注释 Ctrl + /
    批量上移 Ctrl + Shift + ↑
    批量下移 Ctrl + Shift + ↓


"""
import requests


def save_csv(filename, content):
    "保存数据为CSV文件 list 写入"
    fp = open(f'{filename}.csv', 'a+', newline='', encoding='utf-8-sig')
    csv_fp = csv.writer(fp)
    csv_fp.writerow(content)
    fp.close()
    print(f'正在写入:{content}')


header = {
    'Referer': 'https://category.vip.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
    'Cookie': 'vip_address=%257B%2522pid%2522%253A%2522103102%2522%252C%2522cid%2522%253A%2522103102101%2522%252C%2522pname%2522%253A%2522%255Cu6c5f%255Cu82cf%255Cu7701%2522%252C%2522cname%2522%253A%2522%255Cu5357%255Cu4eac%255Cu5e02%2522%257D; vip_province=103102; vip_province_name=%E6%B1%9F%E8%8B%8F%E7%9C%81; vip_city_name=%E5%8D%97%E4%BA%AC%E5%B8%82; vip_city_code=103102101; vip_wh=VIP_SH; vip_ipver=31; mst_area_code=104104; mars_cid=1689250429110_19a247e6d39524f0b2691fcad2474761; mars_sid=201fd1808342ad7a998a0b24ccc28719; mars_pid=0; VIP_QR_FIRST=1; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0%7Cul%3A3105; visit_id=F94D487773639498464C90D941271D2A; user_class=a; vpc_uinfo=fr713%3A0%2Cfr1352%3A0%2Cfr674%3AD1%2Cfr1051%3A0%2Cfr766%3A0%2Cfr259%3AS0-4%2Cfr896%3A0%2Cfr0901%3A0%2Cfr884%3A0%2Cfr863%3A0%2Cfr392%3A310505%2Cfr398%3A0%2Cfr408%3A0%2Cfr251%3AA%2Cfr1195%3A0%2Cfr344%3A0%2Cfr444%3AA%2Cfr848%3A0%2Cfr1196%3A0%2Cfr249%3AA1%2Cfr328%3A3105%2Cfr902%3A0%2Cfr901%3A0%2Cfr980%3A0; vip_tracker_source_from=; pg_session_no=12; vip_access_times=%7B%22list%22%3A7%7D'
}


def get_page(pageOffset):
    link = f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank?app_name=shop_pc&app_version=4.0&warehouse=VIP_SH&fdc_area_id=103102101&client=pc&mobile_platform=1&province_id=103102&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1689250429110_19a247e6d39524f0b2691fcad2474761&wap_consumer=a&standby_id=nature&keyword=%E6%B3%B3%E8%A1%A3&lv3CatIds=&lv2CatIds=&lv1CatIds=&brandStoreSns=&props=&priceMin=&priceMax=&vipService=&sort=0&pageOffset={pageOffset}&channelId=1&gPlatform=PC&batchSize=120&_=1689316409880'
    page_num = math.ceil(pageOffset / 120) + 1
    print(f'正在爬取第{page_num}页')
    print('pageOffset', f'{pageOffset}')
    # print(link)

    response = requests.get(url=link, headers=header)

    if response.status_code == 200:

        # print(response.text)
        products = response.json()['data']['products']

        page_total = response.json()['data']['total']
        print('products', products)  # 商品ID列表
        print('len(products)', len(products))

        '''# products_list = []
        for products_list in products:
            print(products_list['pid'])'''

        pid_lists = [product['pid'] for product in products]

        pid_list1 = pid_lists[:50]
        pid_list2 = pid_lists[50:100]
        pid_list3 = pid_lists[100:]

        pid_list = [pid_list1, pid_list2, pid_list3]

        # for pid in pid_list:
        for i, pid in enumerate(pid_list):
            print('此子页面的商品pid', pid)  # 切片的商品ID列表
            print('len(pid)', len(pid))
            pid_string = ','.join(pid)
            # print('pid_string', pid_string)

            url = f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'
            #       https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2
            params = {
                'app_name': ' shop_pc',
                'app_version': ' 4.0',
                'warehouse': ' VIP_SH',
                'fdc_area_id': ' 103102101',
                'client': ' pc',
                'mobile_platform': ' 1',
                'province_id': ' 103102',
                'api_key': ' 70f71280d5d547b2a7bb370a529aeea1',
                'user_id': ' ',
                'mars_cid': ' 1689250429110_19a247e6d39524f0b2691fcad2474761',
                #             1689250429110_19a247e6d39524f0b2691fcad2474761
                'wap_consumer': ' a',
                'productIds': pid_string,
                # 'productIds':' 6919967848692122900,6919798151514518861,6919172521165554132,6920285508803059228,6920086968587152079,6919986635456665227,6919250795635778132,6919798151514506573,6919221354152415892,6920333096156845268,6919570823605344796,6919675086681596703,6919938807385331604,6920323328092155399,6920224576466925191,6920269775151187284,6920137626444862100,6919073646414612043,6919798151565043021,6919269290708597831,6920404534151400320,6920333096156861652,6920453816872247898,6920292798115451289,6920377028907999367,6920330580854132231,6920311638011276941,6920101520475945679,6920189634053621524,6918915874224063836,6920224576466912903,6920334927451704839,6919827210032574940,6919764953830565520,6920403031213253504,6919259179854452052,6920371115020341959,6920386923071996608,6920397091090039620,6919837579291338844,6919136056805686164,6920334927451713031,6920430261628644295,6918700873957560468,6919675341290738836,6920250903815424655,6920366918282336732,6920346658809823645,2169989739,6920453816872116826,',
                'scene': ' search',
                'standby_id': ' nature',
                'extParams': ' {"stdSizeVids":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x","ic2label":1,"superHot":1,"bigBrand":"1"}',
                'context': ' ',
                '_': ' 1689309574409'

            }

            response = requests.get(url=url, params=params, headers=header)
            # print(response)

            if response.json().get('data') and response.status_code == 200:
                print('response.json()', response.json())
                products_info = response.json()['data']['products']
                # print('products_info', products_info)

                for product in products_info:  # 爬取第一页的3个子页面商品信息
                    # print(product)
                    '''for j in product['attrs']:
                        print(j)
                        attr = j['value']
                        ','.join(attr)'''
                    attr = ','.join([j['value'] for j in product['attrs']])  # 商品信息
                    brandId = product['brandId']  # 品牌id
                    brandShowName = product['brandShowName']  # 品牌名

                    marketPrice = product['price']['marketPrice']  # 原价
                    mixPriceLabel = product['price']['mixPriceLabel']  # 折扣
                    salePrice = product['price']['salePrice']  # 现价
                    productId = product['productId']  # 商品id
                    skuId = product['skuId']  # skuId
                    title = product['title']  # 标题
                    # print(title, attr, brandId, brandShowName, productId, marketPrice, salePrice, mixPriceLabel, skuId)

                    # 标题，商品信息，品牌id，品牌名，商品id，原价，现价，折扣，skuId
                    info_col = [title, attr, brandId, brandShowName, productId, marketPrice, salePrice, mixPriceLabel,
                                skuId]
                    save_csv('泳衣', info_col)

            else:
                print(f'请求第{page_num}页商品第{i+1}个子页面失败', '不存在该商品', '\n')
                with open('请求失败数据.csv', mode='a+', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    sentence = f'请求第{page_num}页商品第{i+1}个子页面失败'
                    writer.writerow([sentence])
                file.close()

            print(f'共有{page_total}条数据,第{page_num}页，第{i + 1}个子页面商品信息({page_num}_{i + 1})-->已保存')

            # 暂停6-20秒
            t = random.randint(6, 20)
            if i == 0 or i == 1:
                print(f'休息{t}秒后，继续爬取第{page_num}整页的下个子页（第{page_num}_{i + 2}页）评论', '\n')
            else:
                print(f'休息{t}秒后，准备爬取第{page_num+1}页，完整页评论', '\n')
            time.sleep(t)

        print(f'第{page_num}页商品信息-->已保存', '\n', '\n')

        # 总页数 = math.ceil(page_total / 120)  # 向上取整  2241/120=18.675  19页
        if page_num > math.floor(page_total / 120):  # math.floor(page_total / 120) 向下取整  # 如果当前页数大于总页数，就停止爬取
            print('爬取完毕')
            sys.exit()  # 退出程序
        else:  # 否则，继续爬取下一页
            page_num += 1
            pageOffset += 120

            get_page(pageOffset)  # 递归调用

    else:
        print(f'请求失败第{page_num}页失败')


if __name__ == '__main__':
    get_page(0)
