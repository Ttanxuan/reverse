# encoding  = utf-8
import requests,re,csv,os
from flashtext import KeywordProcessor
import execjs,subprocess
from loguru import  logger

# 文件名介绍：
# hongshu.js 是从网页源代码中抠出来的，目的是解析第二次请求后得到的加密content（中文字体）,other（字体反爬规则）
# hongshuconfound.js 为解密other后得到的js代码
# ast.js 的目的有二，1是对 hongshuconfound.js 中的代码进行反混淆，反混淆之后进行注释；2是在 hongshuconfound.js 基础上删除无用代码和添加规则代码，使得 after_confound.js 中的代码可以运行
# after_confound.js 的目的是得到反爬字体（如 context_kw1 等对应的中文字体）

# 得到key参数
def get_key(cid):
    logger.info('开始请求key')
    key_re = re.compile('"key":"(.*?)"')
    cookies = {
        '_ga': 'GA1.1.1465078173.1717851259',
        'PHPSESSID': '5e6u2lrch1uha1mlrb3f1e5ea5',
        'Hm_lvt_5268a54e187670ee0953ba36efee746a': '1717851260',
        'Hm_lpvt_5268a54e187670ee0953ba36efee746a': '1717851872',
        'hsclastchapter113772': '%7B%22title%22%3A%22%E7%AC%AC2%E7%AB%A0%20%E6%9C%80%E6%AF%92%E5%A6%87%E4%BA%BA%E5%BF%83%22%2C%20%22bid%22%3A%22113772%22%2C%22jid%22%3A%22205425%22%2C%22cid%22%3A%221466258%22%2C%22curpos%22%3A%222%22%2C%22total%22%3A%221446%22%2C%20%22addtime%22%3A%221717852737%22%7D',
        '_ga_0YS75Q4BJM': 'GS1.1.1717851259.1.1.1717852753.0.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.1.1465078173.1717851259; PHPSESSID=5e6u2lrch1uha1mlrb3f1e5ea5; Hm_lvt_5268a54e187670ee0953ba36efee746a=1717851260; Hm_lpvt_5268a54e187670ee0953ba36efee746a=1717851872; hsclastchapter113772=%7B%22title%22%3A%22%E7%AC%AC2%E7%AB%A0%20%E6%9C%80%E6%AF%92%E5%A6%87%E4%BA%BA%E5%BF%83%22%2C%20%22bid%22%3A%22113772%22%2C%22jid%22%3A%22205425%22%2C%22cid%22%3A%221466258%22%2C%22curpos%22%3A%222%22%2C%22total%22%3A%221446%22%2C%20%22addtime%22%3A%221717852737%22%7D; _ga_0YS75Q4BJM=GS1.1.1717851259.1.1.1717852753.0.0.0',
        'Origin': 'https://www.hongshu.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.hongshu.com/content/113772/205425-1466258.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'method': 'getchptkey',
        'bid': '113772',
        'cid': cid,   # 两次请求cid需要相同
    }

    # proxies，cer设置从fiddler走，利用fiddler抓包
    proxies = {
        'http':'127.0.0.1:10086',
        'https':'127.0.0.1:10086'
    }
    cer = "F:\certificate\certf.cer"

    response = requests.post('https://www.hongshu.com/bookajax.do', cookies=cookies, headers=headers, data=data)    #,verify=cer,proxies=proxies
    # print(response.text)
    key = key_re.findall(response.text)
    return key

# 得到未解密的文字内容和解密文字的js代码
def get_data(cid):
    logger.info('开始请求加密内容')
    content_re = re.compile('"content":"(.*?)","sub')
    other_re = re.compile('"other":(.*?)","')
    nextcid_re = re.compile('"nextcid":"(.*?)"')

    cookies = {
        '_ga': 'GA1.1.1465078173.1717851259',
        'PHPSESSID': '5e6u2lrch1uha1mlrb3f1e5ea5',
        'Hm_lvt_5268a54e187670ee0953ba36efee746a': '1717851260',
        'Hm_lpvt_5268a54e187670ee0953ba36efee746a': '1717856220',
        'hsclastchapter113772': '%7B%22title%22%3A%22%E7%AC%AC11%E7%AB%A0%20%E9%99%AA%E7%BB%83%22%2C%20%22bid%22%3A%22113772%22%2C%22jid%22%3A%22205425%22%2C%22cid%22%3A%221600291%22%2C%22curpos%22%3A%2211%22%2C%22total%22%3A%221446%22%2C%20%22addtime%22%3A%221717856222%22%7D',
        '_ga_0YS75Q4BJM': 'GS1.1.1717854674.2.1.1717856421.0.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.1.1465078173.1717851259; PHPSESSID=5e6u2lrch1uha1mlrb3f1e5ea5; Hm_lvt_5268a54e187670ee0953ba36efee746a=1717851260; Hm_lpvt_5268a54e187670ee0953ba36efee746a=1717856220; hsclastchapter113772=%7B%22title%22%3A%22%E7%AC%AC11%E7%AB%A0%20%E9%99%AA%E7%BB%83%22%2C%20%22bid%22%3A%22113772%22%2C%22jid%22%3A%22205425%22%2C%22cid%22%3A%221600291%22%2C%22curpos%22%3A%2211%22%2C%22total%22%3A%221446%22%2C%20%22addtime%22%3A%221717856222%22%7D; _ga_0YS75Q4BJM=GS1.1.1717854674.2.1.1717856421.0.0.0',
        'Origin': 'https://www.hongshu.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.hongshu.com/content/113772/205425-1600301.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'method': 'getchpcontent',
        'bid': '113772',
        'jid': '205425',
        'cid': cid,
    }
    proxies = {
        'http':'127.0.0.1:10086',
        'https':'127.0.0.1:10086'
    }
    cer = "F:\certificate\certf.cer"

    response = requests.post('https://www.hongshu.com/bookajax.do', cookies=cookies, headers=headers, data=data)    # #,verify=cer,proxies=proxies
    # print(response.text)
    res = []
    
    content = content_re.findall(response.text)[0]
    other = other_re.findall(response.text)[0]
    nextcid = nextcid_re.findall(response.text)[0]
    
    res.append(other)
    res.append(content)
    res.append(nextcid)

    return res

# 使用 flashtext 库进行替换
def flashtext_replace(text, replacements):
    logger.info('开始替换反爬字体')
    processor = KeywordProcessor()
    for key, value in replacements.items():
        processor.add_keyword(key, value)
    return processor.replace_keywords(text)

# 利用集合得到反爬字体的种类
def get_kw(resu):
    logger.info('利用集合得到反爬字体种类')
    kw_re = re.compile("class='context_kw(.*?)'")
    kwlist = kw_re.findall(resu)
    kwset = set(kwlist)
    return kwset

# 将解密的文字替换掉加密文字
def get_replacements(kwset):
    logger.info('开始替换反爬字体')
    replacements = {
    }
    with open('after_confound.js','r') as f:
        js_code = f.read()
        ctx = execjs.compile(js_code)
    for i in kwset:
        res = ctx.call('get_word',i)
        # print(type(ctx))
        replacements.update({f'span class=\'context_kw{i}': f'gt;{res}&lt'})

    # print(replacements)
    return replacements

#
def append_long_string_to_csv(filename, long_string):

    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 如果文件不存在，创建新文件时写入初始内容（可选）
        if not file_exists:
            print(f"File '{filename}' does not exist. Creating new file.")

        # 拆分长字符串并逐行追加
        for line in long_string.splitlines():
            writer.writerow([line])


if __name__ == '__main__':
    start_cid = '1455572'
    next_cid = ''
    for count in range(1):
        if count == 0 :
            cid = start_cid
        else:
            cid = next_cid
            next_cid = ''
        data_re = re.compile('gt;(.*?)&lt')
        key = get_key(cid)[0]
        
        logger.info(f'key:{key}')
        res = get_data(cid)
        logger.info(res)
    
        # 调用js接口得到解密后的文字
        with open('hongshu.js', 'r')as f:
            js_code = f.read()

        ctx = execjs.compile(js_code)

        resu = ctx.call('decrypt_data',res[1],key)
        other = ctx.call('decrypt_data',res[0],key) #得到字体反爬的js解密代码
        next_cid = res[2]

        js_file_path = 'hongshuconfound.js'

        # 使用覆盖模式打开文件，并写入新的 JavaScript 代码
        with open(js_file_path, 'w',encoding='utf-8') as js_file:
            js_file.write(other)
            logger.info('other写入文件')

        # 运行ast.js
        js_file = 'ast.js'
        subprocess.run(['node',js_file])
        logger.info('ast运行完毕')

        kwset = get_kw(resu)    # 得到反爬文字的种类
        logger.info(kwset)

        replacements = get_replacements(kwset)
        logger.info(f'反爬字体种类:{replacements}')
        data_cou = flashtext_replace(resu,replacements)
        # print(data_cou)

        data = data_re.findall(data_cou)
        logger.info(data)
        data_str = ''
        for dt in data:
            if dt != '':
                if dt != '。':
                    data_str += dt
                else:
                    data_str = data_str + dt + '\n' + '  '
        logger.info(data_str)

        # append_long_string_to_csv('./小说.csv',data_str)
        # logger.info(f'下载第{count+1}章')
        # logger.info(data_str)



