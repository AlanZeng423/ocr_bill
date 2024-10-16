import json
# from ocr import extracted_info
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def send(field):
    # 创建client
    client = lark.Client.builder() \
        .app_id("your_app_id") \
        .app_secret("your_app_secret") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateAppTableRecordRequest = CreateAppTableRecordRequest.builder() \
        .app_token("your_app_token") \
        .table_id("table_id") \
        .request_body(AppTableRecord.builder()
            .fields(field)
            .build()) \
        .build()

    # 发起请求
    response: CreateAppTableRecordResponse = client.bitable.v1.app_table_record.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

