from UA import agents
import random
import requests
import json
from lxml import html
import time
import pandas as pd

# redis-server.exe
# cd D:\0主线任务-2-nus\5214\ProxyPool



headers={
'User-Agent':random.choice(agents)
}


xueqiu_url='https://xueqiu.com/'#雪球官网
comment_url= 'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={symbol}&hl=0&source=all&sort=&page={num}&q=&type=11'


stock_pool = pd.read_excel('000300pool.xlsx', header=None).values.flatten().tolist()

# stock = 'SZ000001'

for stock in stock_pool:
    print('正在爬取'+stock)
    result_df = pd.DataFrame()
    session = requests.session()

    proxy = requests.get('http://localhost:5555/random').text  # 获取本地代理池代理
    
    if proxy:
         proxies = {'http': 'http://{}'.format(proxy),
                    'https': 'http://{}'.format(proxy), }
         session.proxies = proxies  # 携带代理

        try:
            # First_request 创建 cookie
            First_request = session.get(url='https://xueqiu.com/', headers=headers)
            print('已获取cookie')
            url = comment_url.format(symbol=stock, num=str(random.randint(1, 10)))
            print('已进入评论页')
            comments_list = session.get(url, headers=headers)
            page = json.loads(comments_list.text)['maxPage']  # 获取最大页数

            for i in range(1, page + 1):
                url = comment_url.format(symbol=stock, num=str(i))  # 股票列表URL
                comments_list = session.get(url, headers=headers, timeout=30)
                if str(comments_list.status_code) == str(200):
                    stocks_comment = json.loads(comments_list.text)['list']
                    for comment in stocks_comment:
                        try:
                            # text = comment.get('text').strip()
                            # selector = html.fromstring(text)  # 里面的标签各种各样，各种嵌套，用正则调了很久，投降了，改用xpath
                            # comment = selector.xpath('string(.)')
                            # comment = stock.get('description')
                            # user_id = stock.get('user_id')  # 评论者ID
                            # user = stock.get('user')  # 评论者信息
                            # title = stock.get('title')  # 标题
                            # comment_id = stock.get('id')  # 每条评论都要唯一的ID

                            # 此处添加数据库操作
                            result_df = result_df._append(comment, ignore_index=True)

                        except:
                            print('评论爬取出现异常')
                            pass

                    print('正在爬取第', str(i), '页, 该股票一共', str(page), '页。')
                    time.sleep(3)

                else:
                    print('第', str(i), '页status_code != 0')
                    pass

            # 抓取到了最后一页
            print(stock, '该股票抓取成功')
            result_df.to_csv(r'./result/'+stock+'xueqiu.csv')


        except Exception as e:
            print('网站拦截，准备重新获取')  # 失败后再来
            time.sleep(10)
            continue

    # else:
    #     print('proxy建立失败')
    #     time.sleep(15)  # 等待重新获取代理
    #     continue
