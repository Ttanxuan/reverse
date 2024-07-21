# encoding  = utf-8
import requests,re,time
import ddddocr
import execjs

# 网址：aHR0cHM6Ly93d3cuZ2VldGVzdC5jb20vYWRhcHRpdmUtY2FwdGNoYS1kZW1v
# https://www.geetest.com/adaptive-captcha-demo

# 第一次请求，得到背景图与缺口的url。同时得到第二次请求中params的参数 lot_number，payload，process_token，与生成w所需的datetime
def get_slideimgurl(slide):
    # 正则匹配
    bg_re = re.compile(',"bg\"\:"(.*?)",\"ypos\"')    # 背景图片url
    slice_re = re.compile('de\"\,\"slice\"\:"(.*?)"')   # 缺口url

    lot_re = re.compile('"lot_number":"(.*?)","cap')    # 参数lot_number
    payload_re = re.compile('"payload":"(.*?)","proc')    # 参数payload
    protk_re = re.compile('"process_token":"(.*?)","pay')    # 参数process_token
    datetime_re = re.compile('datetime":"(.*?)","hashfunc')    # datetime在逆向w时需要用到


    url = 'https://gcaptcha4.geetest.com/load'
    params = {
        'callback': 'geetest_' + str(int(time.time()*1000)),
        'captcha_id': '24f56dc13c40dc4a02fd0318567caef5',
        'challenge': 'e35d7241-f956-4f0d-a234-4a3fdc10a58e',
        'client_type': 'web',
        'risk_type': slide,   # slide为滑块，word为点选
        'lang': 'zh'
        }
    # print(params)
    headers = {
        'Referer':'https://www.geetest.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,params=params,headers=headers)
    # print(resp.text)

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
    bg_img = requests.get(bg_url).content
    with open('../背景图.png', 'wb+') as f:
        f.write(bg_img)

    slice_img = requests.get(slice_url).content
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

    # 编译生成w的js代码
    with open('极验滑块4.js', 'r', encoding='utf-8') as file:
        js_code = file.read()

    ctx = execjs.compile(js_code)

    # 传入参数 得到w
    w = ctx.call('get_w',params_bas['setLeft'],params_bas['lot_number'],params_bas['datetime'])


    url = 'https://gcaptcha4.geetest.com/verify'
    params = {
        'callback': 'geetest_' + str(int(time.time()*1000)),
        'captcha_id': '24f56dc13c40dc4a02fd0318567caef5',
        'client_type': 'web',
        'lot_number': params_bas['lot_number'],
        'risk_type': 'slide',
        'payload': params_bas['payload'],
        'process_token': params_bas['process_token'],
        'payload_protocol': '1',
        'pt': '1',
        'w':w
    }
    print(params)
    headers = {
        'Referer':'https://www.geetest.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,params=params,headers=headers)
    print(resp.text)



if __name__ == '__main__':
    risk_type = {
        'slide':'slide',
        'word':'word'
    }
    bg_url,slice_url,params_bas = get_slideimgurl(risk_type['slide'])

    result = get_img(bg_url, slice_url)

    params_bas['setLeft'] = result['target'][0]
    print(params_bas)

    verify(params_bas)


