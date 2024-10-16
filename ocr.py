 # /**********************************************************
#  * Author: AlanZeng
#  * Email: me@alanzeng.com
#  * Created on: 2024-10-16 00:57:13
#  * Description:
#  **********************************************************/

from PIL import Image
import pytesseract
import re
from send import send
from datetime import datetime

# 定义日期格式
date_format = '%Y-%m-%d %H:%M:%S'



# Update the path to Tesseract if required
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this if necessary

def extract_info(text):
    # 提取金额
    amount_match = re.search(r'[-\d,]+\.\d{2}', text)
    amount = amount_match.group(0).replace('-', '').replace(',', '').strip() if amount_match else None
    amount = float(amount) if amount else None

    # 提取付款时间
    payment_time_match = re.search(r'支付时间 (.*?)\n', text)
    payment_time = payment_time_match.group(1).lstrip().strip() if payment_time_match else None
    payment_time_dt = datetime.strptime(payment_time, date_format) if payment_time else None
    payment_unix_timestamp = int(payment_time_dt.timestamp())*1000 if payment_time_dt else None



    # 提取商品说明
    product_description_match = re.search(r'商品说明 (.+?)(?=\n)', text)
    product_description = product_description_match.group(1).replace(' ', '').strip() if product_description_match else None

    # 提取付款方式
    payment_method_match = re.search(r'付款方式 (.+?)(?= >)', text)
    payment_method = payment_method_match.group(1).replace(' ', '').strip() if payment_method_match else None

    # return {
    #     "金额": amount,
    #     "商品说明": product_description,
    #     "付款方式": payment_method
    # }
    return {
        "Amount": amount,
        "Remarks": product_description,
        "Income/Expense Item": payment_method,
        "Date": payment_unix_timestamp
        # "Date": payment_time
    }



# Load the image
img_paths = [
    'Screenshot 2024-10-16 at 00.55.19.jpeg', 
    'Screenshot 2024-10-16 at 01.17.11-1.jpeg',
    'Screenshot 2024-10-16 at 01.17.07.jpeg',
    ]  # Update this with your image path
# img_path = 'Screenshot 2024-10-16 at 00.55.19.jpeg'  # Update this with your image path
# img = Image.open(img_path)

# Use Tesseract to do OCR on the image
def ocr(img_path):
    # for img_path in img_paths:
    img = Image.open(img_path)

    text = pytesseract.image_to_string(img, lang='chi_sim')  # Use 'chi_sim' for simplified Chinese
    print(text)
    # Output the extracted text
    # print(text)

    # 提取信息并打印
    extracted_info = extract_info(text)
    print(extracted_info)
    send(extracted_info)

    # 提取金额、商品说明和付款方式

# if __name__ == '__main__':
#     main()

# for i in img_paths:
#     ocr(i)