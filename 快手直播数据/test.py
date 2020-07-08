import requests
import json
session = requests.session()
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
           'Host': 'www.bihukankan.com',
           'Cookie': 'Hm_lvt_348822e7d440f6b751ed21d40cf5b66d=1592894288; gr_user_id=977640de-a40a-4382-b575-504ecab9e2eb; a57cc8401368a31b_gr_session_id=8012a354-7be9-4edf-bb85-fdf489ad2542; a57cc8401368a31b_gr_session_id_8012a354-7be9-4edf-bb85-fdf489ad2542=true; grwng_uid=003120bb-159d-46d1-9d64-bf8206e03ea4; _ga=GA1.2.428395723.1592894288; _gid=GA1.2.216034712.1592894288; _gat_gtag_UA_142459456_1=1; Hm_lpvt_348822e7d440f6b751ed21d40cf5b66d=1592894337'
           }
url = 'https://www.bihukankan.com/apiCarrierList?road=liveStreamECommerce&index=1&page=25&sort=eCommerceIndex&order=desc&time=%7B%24between%3A%20%5B1592755200%2C%201592841599%5D%7D'
r = session.get(url, headers=headers)
print(r.status_code)
# print(r.text)
print(session.cookies)

reulse = json.loads(r.text)
datas = reulse.get('data')
count = 1
print(len(datas))