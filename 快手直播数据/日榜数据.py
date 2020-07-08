import os
import json
import requests
import pandas as pd


def daily():
    """日榜数据"""
    url = 'https://www.bihukankan.com/apiCarrierList?road=liveStreamECommerce&index=1&page=25&sort=eCommerceIndex&order=desc&time=%7B%24between%3A%20%5B1592755200%2C%201592841599%5D%7D'
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Host': 'www.bihukankan.com',
               'Cookie': 'gr_user_id=94760feb-9ff9-4ede-9a29-b53d0274c6c1; grwng_uid=2cea0801-1dd5-4f28-b2e1-99d0bcc84134; _ga=GA1.2.213601449.1592802703; _gid=GA1.2.1011567398.1592802703; Hm_lvt_348822e7d440f6b751ed21d40cf5b66d=1592802701,1592819229; token=430ad05680488a92c495624341b930f7297a11a673bf403db5296d51fb9df348e14083ca024d3b7f5fbe38014129e09a6f9aae8126266dde6aa8ded9c8e21abeaf66d2234cc3a18c5a10cf33176658c9363356decc60010b040249dcfba1bec7daf2e3dbf1cfdfaf%3B%20Max-Age; a57cc8401368a31b_gr_session_id=ffc52d23-2158-4b9c-94d2-e833a1e0147e; Hm_lpvt_348822e7d440f6b751ed21d40cf5b66d=1592882385; a57cc8401368a31b_gr_session_id_ffc52d23-2158-4b9c-94d2-e833a1e0147e=true'
               }
    res = requests.get(url, headers=headers, timeout=30)
    print(res.status_code)
    reulse = json.loads(res.text)
    datas = reulse.get('data')
    count = 1
    print(len(datas))
    print(reulse.get('paging'))
    for i in range(len(datas)-1):
        id = datas[i].get('anchor').get('id')  # bihukankan id
        name = datas[i].get('anchor').get('name')  # 用户名
        userid = datas[i].get('anchor').get('userId')  # 快手ID
        fans = datas[i].get('anchor').get('fans')  # 粉丝数
        avatar = datas[i].get('anchor').get('avatar')  # 头像

        tag = '-'.join(datas[i].get('tag'))  # 主播所属分类
        _time = datas[i].get('time')  # 数据时间
        receiveGift = datas[i].get('receiveGift')  # 接收礼物
        duration = datas[i].get('duration')  # 直播时长
        sales = datas[i].get('sales')  # 总销售额
        salesVolume = datas[i].get('salesVolume')  # 总销量
        commodityCount = datas[i].get('commodityCount')  # 商品数量
        sourceType = datas[i].get('sourceType')  # 直播类型
        maxViews = datas[i].get('maxViews')  # 最大观看次数
        createdAt = datas[i].get('createdAt')  # 创建时间
        updatedAt = datas[i].get('updatedAt')  # 更新时间
        salesRank = datas[i].get('salesRank')  # 带货能力
        content = {'id': id, '用户名': name, '快手ID': userid, '粉丝数': fans, '头像': avatar, '主播所属分类': tag, '数据时间': _time,
                   '接收礼物': receiveGift, '直播时长': duration, '总销售额': sales, '总销量': salesVolume, '商品数量': commodityCount,
                   '直播类型': sourceType, '最大观看次数': maxViews, '创建时间': createdAt, '更新时间': updatedAt, '带货能力': salesRank
                   }
        save_xls(content)
        print(f'第:{count}条数据保存成功!')
        count += 1


def save_xls(data):
    """
    保存数据
    data : 字典格式 必须和表头长度一样
    :return:
    """
    path = os.path.abspath('.') + r'/日榜数据.xls'
    if not os.path.exists(path):
        # 创建一个新DataFrame并添加表头
        Header = ['id', '用户名', '快手ID', '粉丝数', '头像', '主播所属分类', '数据时间', '接收礼物', '直播时长',
                  '总销售额', '总销量', '商品数量', '直播类型', '最大观看次数', '创建时间', '更新时间', '带货能力']
        df = pd.DataFrame(columns=Header)
    else:
        df_read = pd.read_excel(path)
        df = pd.DataFrame(df_read)

    # 定义一行新数据 data为一个字典
    new = pd.DataFrame(data, index=[1])  # 自定义索引为：1 ，这里也可以不设置index

    # 把定义的新数据添加到原数据最后一行 ignore_index=True,表示不按原来的索引，从0开始自动递增
    df = df.append(new, ignore_index=True)

    # 保存数据 sheet_name工作表名 index是否添加索引 header表头
    df.to_excel(path, sheet_name='data', index=False, header=True)


if __name__ == '__main__':
    daily()
