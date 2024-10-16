
import requests
import json
import base64
from datetime import datetime
import time
from send import send


def baidu_ocr(img_path):
    api_key = ""
    secret_key = ""
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + api_key + "&client_secret=" + secret_key
    # url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xxxxxx&client_secret=xxxxx"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    response = json.loads(response.text)
    access_token = response['access_token']
    print(f"access_token: {access_token}")

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (f"response ok")
        
    ocr_result = response.json()

    # 初始化变量
    amount = None
    product_description = None
    payment_method = None
    payment_time = None

    # 遍历 OCR 结果，提取需要的信息
    for i, item in enumerate(ocr_result['words_result']):
        text = item['words']
        
        # 提取金额
        if '-' in text and text.replace(',', '').replace('-', '').replace('.', '').isdigit():
            amount = float(text.replace(',', '').replace('-', '').strip())
        
        # 动态提取商品说明（根据“商品说明”后面的文字）
        if '商品说明' in text and i + 1 < len(ocr_result['words_result']):
            product_description = ocr_result['words_result'][i + 1]['words']
        
        # 提取付款方式
        if '付款方式' in text and i + 1 < len(ocr_result['words_result']):
            payment_method = ocr_result['words_result'][i + 1]['words'].replace('>', '')
        
        # 提取支付时间
        if '支付时间' in text and i + 1 < len(ocr_result['words_result']):
            payment_time = ocr_result['words_result'][i + 1]['words']

    # 将支付时间转换为 Unix 时间戳
    payment_unix_timestamp = None
    if payment_time:
        try:
            dt_obj = datetime.strptime(payment_time, '%Y-%m-%d%H:%M:%S')
            payment_unix_timestamp = int(time.mktime(dt_obj.timetuple()))
        except ValueError:
            print("Invalid date format")

    # 返回结果
    result = {
        "Amount": amount,
        "Remarks": product_description,
        "Income/Expense Item": payment_method,
        "Date": payment_unix_timestamp*1000  # Unix 时间戳
        # "Date": payment_time  # 如果不需要 Unix 时间戳，可以改为返回支付时间字符串
    }

    print(result)
    send(result)