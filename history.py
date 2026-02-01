import json
import os
import sys

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

# 尝试导入配置文件，如果不存在则使用占位符
try:
    from config import APP_ID, APP_SECRET, CONTAINER_ID, START_TIME, END_TIME
except ImportError:
    print("警告: 未找到 config.py 文件")
    print("请复制 config.example.py 为 config.py 并填入你的配置信息")
    sys.exit(1)


def history():
    # 创建client
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 分页标记，第一次请求时不传递该参数
    page_token = None

    while True:
        # 构造请求对象
        request_builder = ListMessageRequest.builder() \
            .container_id_type("chat") \
            .container_id(CONTAINER_ID) \
            .start_time(START_TIME) \
            .end_time(END_TIME) \
            .sort_type("ByCreateTimeAsc") \
            .page_size(50)

        # 仅在page_token有值时添加到请求中
        if page_token:
            request_builder.page_token(page_token)

        request = request_builder.build()

        # 发起请求
        response: ListMessageResponse = client.im.v1.message.list(request)

        # 输出接口响应的所有内容
        print(f"接口响应内容: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            break

        # 获取新的分页标记
        page_token = response.data.page_token

        # 如果没有更多数据，退出循环
        if not page_token:
            break


if __name__ == "__main__":
    history()