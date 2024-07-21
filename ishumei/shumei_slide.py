# encoding  = utf-8
import requests,re,time,ddddocr
from loguru import logger
from datetime import datetime

re_role = {
    'organization':re.compile('organization:"(.*?)",'),
    'requestId':re.compile('"requestId":"(.*?)",'),
    'bg_jpg':re.compile('"bg":"(.*?)",'),
    'fg_png':re.compile('"fg":"(.*?)",'),
    'k':re.compile('"k":"(.*?)",'),
    'l':re.compile('"l":(.*?),'),
    'rid':re.compile('"rid":"(.*?)"}')
}

def proxies_0(num):
    if num == 1:    # 设置海外ip
        proxies = {
            'http':'127.0.0.1:7897',
            'https':'127.0.0.1:7897'
        }
    elif num == 2:  # 设置fiddler代理
        proxies = {
            'http': '127.0.0.1:10086',
            'https': '127.0.0.1:10086'
        }
    else:
        proxies = {}
    return proxies

# 请求得到organization，可能是身份参数，可固定
def get_org():
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # cookie可能需要改
        'cookie': 'ISHUMEI_WWW_userUid=2866073a-8313-4507-953e-4c65e5545d47; Hm_lvt_b96d87c9b1b6a130a14b9fc14dc746c1=1721563828; Hm_lpvt_b96d87c9b1b6a130a14b9fc14dc746c1=1721563828; HMACCOUNT=135DEA475AA0E00B; Qs_lvt_331993=1721563828; Qs_pv_331993=3900484836640253000; smidV2=20240721201028f295d3516acd326cf4f7ec3fd226bcaa009d666c913548590; __root_domain_v=.ishumei.com; __bid_n=190d53355c24512cb13aca; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190d533565717-0f2eea703b8ec88-26001f51-1327104-190d533565970%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwZDUzMzU2NTcxNy0wZjJlZWE3MDNiOGVjODgtMjYwMDFmNTEtMTMyNzEwNC0xOTBkNTMzNTY1OTcwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190d533565717-0f2eea703b8ec88-26001f51-1327104-190d533565970%22%7D; _qddaz=QD.970021563829672; _qdda=3-1.1; _qddab=3-oct7sm.lyvinljv',
        'pragma': 'no-cache',
        'priority': 'u=2',
        'referer': 'https://www.ishumei.com/trial/captcha.html',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.ishumei.com/static/js/trial/captcha_7867b6f.js', headers=headers,proxies=proxies_0(1))
    logger.info(response.text)
    orgzn = re_role['organization'].findall(response.text)
    logger.info(orgzn)
    return orgzn

def get_register():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ishumei.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ishumei.com/trial/captcha.html',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    now = datetime.now()

    # 格式化成所需的字符串形式：YYYYMMDDHHMMSS
    formatted_now = now.strftime('%Y%m%d%H%M%S')
    captchaUuid = formatted_now + 'FWx2C5Eadz4D62PyJp'
    params = (
        ('organization', 'd6tpAY1oV0Kv5jRSgxQr'),
        ('appId', 'default'),
        ('sdkver', '1.1.3'),
        ('captchaUuid', captchaUuid),    # captchaUuid前14位为时间，后18位为随机数，可写死
        ('callback', 'sm_' + str(int(time.time()*1000))),
        ('rversion', '1.0.4'),
        ('data', '{}'),
        ('channel', 'DEFAULT'),
        ('lang', 'zh-cn'),
        ('model', 'slide'),
    )

    response = requests.get('https://captcha1.fengkongcloud.cn/ca/v1/register', headers=headers, params=params,proxies=proxies_0(1))
    # logger.info(response.text)
    result = []
    result.append(re_role['bg_jpg'].findall(response.text))
    result.append(re_role['fg_png'].findall(response.text))
    result.append(re_role['k'].findall(response.text))
    result.append(re_role['rid'].findall(response.text))
    result.append(captchaUuid)
    return result

def get_slide_match(result_reg):
    # 下载图片
    bg_img = requests.get('https://castatic.fengkongcloud.cn'+result_reg[0][0]).content
    with open('../背景图.png', 'wb+') as f:
        f.write(bg_img)

    slice_img = requests.get('https://castatic.fengkongcloud.cn'+result_reg[1][0]).content
    with open('../缺口.png', 'wb+') as f:
        f.write(slice_img)

    # 识别缺口
    det = ddddocr.DdddOcr(det=False, ocr=False)

    with open('../缺口.png', 'rb') as f:
        target_bytes = f.read()

    with open('../背景图.png', 'rb') as f:
        background_bytes = f.read()

    # 返回数组（缺口坐标）
    result = det.slide_match(target_bytes, background_bytes, True)
    logger.info(result)
    return result


def get_fverify(result_reg):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ishumei.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ishumei.com/trial/captcha.html',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = (
        ('callback', 'sm_' + str(int(time.time()*1000))),
        ('mp', 'WYfkIZp7GoA='),
        ('je', 'FrCa6554swNf4h2fZ+pk98D0Xh5T4Z8L'),
        ('sdkver', '1.1.3'),
        ('ostype', 'web'),
        ('oc', 'h9oFKi8cHpg='),
        ('mu',
         'XUJPJgJ25MfRSXpd2lwYjVTG/RXSL3M9r4sH7U6/lH/9UaRZ0LUA9+0fjpvPKaGaJDdu9rDcSkv+JoXDXrexqSn4V5n64T0so8owGlBvCkp9V3BFb9za56z5XbHiPr3JBC23im9yqtGkiCp7/jXyaM0guBMpJa+Q1PiMIiXsAKr8y03sWcUO8ZFjU6AQACXGrCimsgbTtDiWgUY/EyOmNPm5lY/lqe6atFZvaQH64CkQaRqC51Gqnt7CcSJyrAvTa5Q4Uc/sliWLSXZyoHcV7zDTH69hIgYoqB+tGjHK9k45FQNXJnViboZrAiltRRPtErbcs5yES41PV91h/nJcg+uIUg35l41wIKXejiGgRMAMLP4hrBo95vbXculNzc+35av+lqV0epFyRyVTD39KWlAUKsi2VpCCNZMgpOJj0/rUPKOeaaoBdQyMUC2AMtqtDyzoQvW9rVb2sfEB6YLRQR3RZbhXnZ1FRXYVQ/sbLT3+tFB1ZpllVpxX2vWzAPaWrUA1l/BQKD172ZcAf0UWB76z32U5PDKWbY7Tk7lrJlp+8lJQ8CqkziMEDdJB5WZretunxGG98Gktdaljy4n6uQ=='),
        ('tb', '3jSn4gNaAVM='),
        ('jo', 'l3aEINYnwpY='),
        ('rversion', '1.0.4'),
        ('dy', 'Rfpr5oqb5y4='),
        ('act.os', 'web_pc'),
        ('xy', 'YabT6nmJOC0='),
        ('nu', 'C0kH/bWLjw8='),
        ('organization', 'd6tpAY1oV0Kv5jRSgxQr'),
        ('protocol', '180'),
        ('rid', result_reg[3]),
        ('en', 'y+ugz9NIWys='),
        ('kq', 'mtlOTdT5LOE='),
        ('captchaUuid', result_reg[4]),
        ('ww', 'SZ9Bj8v8yn0='),
    )

    response = requests.get('https://captcha1.fengkongcloud.cn/ca/v2/fverify', headers=headers, params=params,proxies=proxies_0(1))
    return

if __name__ == '__main__':
    # get_org() # 获取本地电脑的请求得到organization参数
    result_reg = get_register()
    get_slide_match(result_reg)
