# encoding  = utf-8
# encoding  = utf-8
import requests,re,time
import ddddocr
import execjs


# 第一次请求，得到背景图与缺口的url。同时得到第二次请求中params的参数 lot_number，payload，process_token，与生成w所需的datetime
def get_slideimgurl():
    # 正则匹配
    bg_re = re.compile('"bg":"(.*?)",')    # 背景图片url
    slice_re = re.compile('"slice":"(.*?)",')   # 缺口url

    lot_re = re.compile('"lot_number":"(.*?)",')    # 参数lot_number
    payload_re = re.compile('"payload":"(.*?)",')    # 参数payload
    # "payload":"_b-sD20eax9oEJvmoMxvFPhrFR891Uk-xRd5rcxJuQKgMqk4ldPYAFje3MYc5D5ho4RGjdhtr8Ezz5gQhkCeTRnNQjvmUjKPr4mIbjosu2iJ1arGhxYxKS1bZrbBYcewwwgbyinvT3sEZ3MfNmvfTh0vTsvXyHqTggRMH0BNLOc9XC_jpWGQWEdUFwvM75J1_dy1jMeFxI_zVfbeMFXkTEYWA7QTAZqoY45QHnFTLCN0BEzUgAWKscTOepAy2PeM3tFi1h2Y4wiMg_8CB1zqDwjNBIAyNjp2dzL61wvJYnzylsF71O-cJ_E-6GOGNtSMvY8thxsPCQSD9XdAvPy55_M2e1eyBg321FtteqZZ5DwN0MKGTUZENr-HC7amv22GUcjaBrMaHT06oRtz7mRacAOHnH7suaeeHisWi5z6F9pCdCAj6AEUy8YHGbPKo2DNXQk9feFWO4HMJFfDaRf-91Nz3548uiZaQtKuKvEECJfmwf_RIJJynGAS1YCqa5skg9VG8ssbeZ1yyW3crKABQzao_N47-YazgpAMXjPc6OMebwsVSx4XoagR44tHT1PRhmXI8F_pXqsmQ_9MlQ2Xdfblzo0w4tr-paaOgEw-0j1BlW47RR98ESJsG4yTz1zUqL49xhUmZxRHCXpFlZ9Z1YmBm54LqUYelqiY0G0cl_zxMI_Mf8O47kvTenc1RaqS4mMOSVqTQHOvg-Tu2UXrcZmh5YM3P7QBoaB7YM4tyB0agf5opdh8Ev6_P9bzGU6j7EQhx_GKMa6KYirhBTrGcS-kXrQoHviMUo2UgKvv38aDqCamP2mRW69jBImVoYcRa-4zi9DJwSDHIu0wfkUUgLGFNvO_N8FC83Hme_2o2tw=","process_token":"c78ccdcffa1f46d1f2fba6cbf138ad47432d4c0974fbd959659e712bcebb8529","payload_protocol":1}})
    protk_re = re.compile('"process_token":"(.*?)",')    # 参数process_token
    datetime_re = re.compile('datetime":"(.*?)","hashfunc')    # datetime在逆向w时需要用到


    url = 'https://gcaptcha4.geetest.com/load'
    params = {
        'callback': 'geetest_' + str(int(time.time()*1000)),
        'captcha_id': '66c1b4d0e33195fd0331baeb26f25999',
        'challenge': '8658bf2b-1947-486b-85c9-922bf9b80df9',
        'client_type': 'web',
        # 'risk_type': slide,   # slide为滑块，word为点选
        'lang': 'zh'
        }
    # print(params)
    headers = {
        'Referer':'https://passport.threatbook.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,params=params,headers=headers )
    print(resp.text)

    # 第二次请求所需参数
    params_bas = {
        'lot_number':lot_re.findall(resp.text)[0],
        'payload': payload_re.findall(resp.text)[0],
        'process_token': protk_re.findall(resp.text)[0],
        'datetime': datetime_re.findall(resp.text)[0]
    }

    # print(bg_re.findall(resp.text)[0])
    # print(slice_re.findall(resp.text)[0])
    # print(params_bas['lot_number'])
    # print(params_bas['payload'])
    # print(params_bas['process_token'])
    # print(params_bas['datetime'])

    # 拼接图片url
    base_url = 'https://static.geetest.com/'
    bg_url = base_url + bg_re.findall(resp.text)[0]
    slice_url = base_url + slice_re.findall(resp.text)[0]

    # 返回url和第二次请求所需参数
    return bg_url,slice_url,params_bas


# 下载图片
def get_img(bg_url,slice_url):

    # 下载图片
    bg_img = requests.get(bg_url ).content
    with open('../背景图.png', 'wb+') as f:
        f.write(bg_img)

    slice_img = requests.get(slice_url ).content
    with open('../缺口.png', 'wb+') as f:
        f.write(slice_img)

    # 识别缺口
    det = ddddocr.DdddOcr(det=False, ocr=False)

    with open('../缺口.png', 'rb') as f:
        target_bytes = f.read()

    with open('../背景图.png', 'rb') as f:
        background_bytes = f.read()

    # 返回数组（缺口坐标）
    result = det.slide_match(target_bytes, background_bytes,True)
    print(result)
    return result

# 第二次请求
def verify(params_bas):
    re_cap_out = re.compile('"captcha_output":"(.*?)"}')
    re_pas_tok = re.compile('"pass_token":"(.*?)",')

    # 编译生成w的js代码
    with open('极验滑块4.js', 'r', encoding='utf-8') as file:
        js_code = file.read()

    ctx = execjs.compile(js_code)

    # 传入参数 得到w
    w = ctx.call('get_w',params_bas['setLeft'],params_bas['lot_number'],params_bas['datetime'])


    url = 'https://gcaptcha4.geetest.com/verify'
    params = {
        'callback': 'geetest_' + str(int(time.time()*1000)),
        'captcha_id': '66c1b4d0e33195fd0331baeb26f25999',
        'client_type': 'web',
        'lot_number': params_bas['lot_number'],
        'payload': params_bas['payload'],
        'process_token': params_bas['process_token'],
        'payload_protocol': '1',
        'pt': '1',
        'w':w
    }
    # print(params)
    headers = {
        'Referer':'https://passport.threatbook.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,params=params,headers=headers )
    print(resp.text)
    token = {
        "captcha_output":re_cap_out.findall(resp.text)[0],
        "pass_token":re_pas_tok.findall(resp.text)[0],
        "lot_number":params_bas['lot_number']
    }
    return token


# 登录
def loginGetTokenForX(token):
    re_data = re.compile('"data":"(.*?)",')
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221911d8877edc4d-09da24f1523e3a-26001e51-1327104-1911d8877eed9b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxMWQ4ODc3ZWRjNGQtMDlkYTI0ZjE1MjNlM2EtMjYwMDFlNTEtMTMyNzEwNC0xOTExZDg4NzdlZWQ5YiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221911d8877edc4d-09da24f1523e3a-26001e51-1327104-1911d8877eed9b%22%7D',
        'origin': 'https://passport.threatbook.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://passport.threatbook.cn/login?service=x&callbackURL=https://x.threatbook.com/v5/node/db3fae7d2dd14bf0/8963c70f2b71019b?redirectURL=https%3A%2F%2Fx.threatbook.com%2Fv5%2Fdomain%2Fdu.testjj.com',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    data = '{"phone_number":"12eswaA","password":"1qa13wsx","is_remember":true,"lot_number":"'+token['lot_number']+'","captcha_output":"'+token['captcha_output']+'","pass_token":"'+token['pass_token']+'","gen_time":"'+str(int(time.time()*1000))+'","plateform":"x"}'

    response = requests.post('https://passport.threatbook.cn/userApi/user/loginGetTokenForX', headers=headers,
                             data=data)
    print(response.text)




if __name__ == '__main__':
    bg_url,slice_url,params_bas = get_slideimgurl()

    result = get_img(bg_url, slice_url)

    params_bas['setLeft'] = result['target'][0]
    # print(params_bas)

    token = verify(params_bas)
    loginGetTokenForX(token)


