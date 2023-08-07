import requests

cookies = {
    'cna': 'bvTaG6TOA2YCAXAC/iAL77TQ',
    'tracknick': '%5Cu7533%5Cu6D41zhao',
    'enc': 'j0Oa74%2BBu%2FZuR78NCNc15Bn5frsIzl%2B0mnRGYRn2WUFCx%2BdcRx63ESKQLLN7TrDE1Q77LRUj193%2BoebLor7smg%3D%3D',
    'thw': 'cn',
    'hng': 'GLOBAL%7Czh-CN%7CUSD%7C999',
    '_uetvid': '1302b410dcef11ed9270f55c590e23d3',
    '_ga': 'GA1.2.498688842.1681715486',
    '_ga_YFVFB9JLVB': 'GS1.1.1683095895.3.1.1683095912.0.0.0',
    'sgcookie': 'E100lUhnPH22NvZjU3ISon5TagAKkTqF0f9jQriThjZGKwx3ZdGOna1pnQ1%2BL9UlfThM3kuOfnsvNhYirIdOutklkaEe9j7%2BqLm%2B2ummr7kx8tY6WqSszroGUxY9SdaUXZct',
    '_cc_': 'WqG3DMC9EA%3D%3D',
    '_m_h5_tk': '44b86d23c42d492ace83cf8528721553_1689867196868',
    '_m_h5_tk_enc': 'fca34be450d9c42ce691e154052e6796',
    'alitrackid': 'www.taobao.com',
    'lastalitrackid': 'www.taobao.com',
    'xlly_s': '1',
    'JSESSIONID': 'CB681B6C7F431516C643391F13017A40',
    'isg': 'BAsLXiXX62ulazDyC45bhE1Ymq_1oB8iw4fyPH0I58qhnCv-BXCvcqk-dpxyp3ca',
    'l': 'fBExBxTcT1MQzFbSBOfaFurza77OSIRYYuPzaNbMi9fP_71B5SpCW1_1Fj86C3GVF6PvR3ooemlBBeYBqQAonxv92j-la_kmndLHR35..',
    'tfstk': 'd0hDH8va8xyjYh0MjsFXMV6_jEp-liN_hcCTX5EwUur5MRr9hc2iX0wZMS3xqloKjPhx6fD5s2gsMEN9lSgb15-pvBhilqN6e0-p9i04GZPwvHdp9qgb15lOzcPlnD0Vls1ATjh78amN_1ly1-qnuOCN_b40ntgVQAWPL1yF1z8taO6_3zauvM6FX_f..',
}

headers = {
    'authority': 's.taobao.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'cna=bvTaG6TOA2YCAXAC/iAL77TQ; tracknick=%5Cu7533%5Cu6D41zhao; enc=j0Oa74%2BBu%2FZuR78NCNc15Bn5frsIzl%2B0mnRGYRn2WUFCx%2BdcRx63ESKQLLN7TrDE1Q77LRUj193%2BoebLor7smg%3D%3D; thw=cn; hng=GLOBAL%7Czh-CN%7CUSD%7C999; _uetvid=1302b410dcef11ed9270f55c590e23d3; _ga=GA1.2.498688842.1681715486; _ga_YFVFB9JLVB=GS1.1.1683095895.3.1.1683095912.0.0.0; sgcookie=E100lUhnPH22NvZjU3ISon5TagAKkTqF0f9jQriThjZGKwx3ZdGOna1pnQ1%2BL9UlfThM3kuOfnsvNhYirIdOutklkaEe9j7%2BqLm%2B2ummr7kx8tY6WqSszroGUxY9SdaUXZct; _cc_=WqG3DMC9EA%3D%3D; _m_h5_tk=44b86d23c42d492ace83cf8528721553_1689867196868; _m_h5_tk_enc=fca34be450d9c42ce691e154052e6796; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; xlly_s=1; JSESSIONID=CB681B6C7F431516C643391F13017A40; isg=BAsLXiXX62ulazDyC45bhE1Ymq_1oB8iw4fyPH0I58qhnCv-BXCvcqk-dpxyp3ca; l=fBExBxTcT1MQzFbSBOfaFurza77OSIRYYuPzaNbMi9fP_71B5SpCW1_1Fj86C3GVF6PvR3ooemlBBeYBqQAonxv92j-la_kmndLHR35..; tfstk=d0hDH8va8xyjYh0MjsFXMV6_jEp-liN_hcCTX5EwUur5MRr9hc2iX0wZMS3xqloKjPhx6fD5s2gsMEN9lSgb15-pvBhilqN6e0-p9i04GZPwvHdp9qgb15lOzcPlnD0Vls1ATjh78amN_1ly1-qnuOCN_b40ntgVQAWPL1yF1z8taO6_3zauvM6FX_f..',
    'referer': 'https://www.taobao.com/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
}

params = {
    'q': '苹果14',
    'suggest': '0_1',
    'commend': 'all',
    'ssid': 's5-e',
    'search_type': 'item',
    'sourceId': 'tb.index',
    'spm': 'a21bo.jianhua.201856-taobao-item.2',
    'ie': 'utf8',
    'initiative_id': 'tbindexz_20170306',
    '_input_charset': 'utf-8',
    'wq': '苹果',
    'suggest_query': '苹果',
    'source': 'suggest',
}

response = requests.get('https://s.taobao.com/search', params=params, cookies=cookies, headers=headers)
print(response.json())
