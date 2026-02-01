import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import csv
import sys

# 尝试导入配置文件
try:
    from config import APP_ID, APP_SECRET, OUTPUT_CSV, REACTION_JSON
except ImportError:
    print("警告: 未找到 config.py 文件")
    print("请复制 config.example.py 为 config.py 并填入你的配置信息")
    sys.exit(1)


def get_message_ids():
    """从output.csv获取message_id列表"""
    message_ids = []
    csv_file = OUTPUT_CSV if 'OUTPUT_CSV' in dir() else 'output.csv'

    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'message_id' not in reader.fieldnames:
                print("错误: CSV文件中未找到'message_id'列")
                return []
            message_ids = [row['message_id'] for row in reader]
            # 过滤空值
            message_ids = [mid for mid in message_ids if mid.strip()]
    except FileNotFoundError:
        print(f"错误: 未找到 {csv_file} 文件")
        print("请先运行 analysis.py 生成 CSV 文件")
    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
    return message_ids


def get_all_reactions(client, message_id):
    """获取指定消息的所有reaction_id总数(处理分页)"""
    page_token = None
    total_count = 0

    while True:
        # 构造请求构建器
        request_builder = ListMessageReactionRequest.builder() \
            .message_id(message_id) \
            .page_size(50)  # 设置每页大小

        # 仅在page_token有值时添加到请求中
        if page_token:
            request_builder.page_token(page_token)

        request = request_builder.build()

        # 发起请求
        response = client.im.v1.message_reaction.list(request)

        # 输出接口响应的所有内容(调试用)
        print(
            f"消息 {message_id} 接口响应内容: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"获取消息 {message_id} 的reaction失败, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            break

        # 累加当前页的reaction数量
        if response.data and response.data.items:
            total_count += len(response.data.items)

        # 获取新的分页标记
        page_token = response.data.page_token if (response.data and hasattr(response.data, 'page_token')) else None

        # 如果没有更多数据，退出循环
        if not page_token:
            print(f"消息 {message_id} 没有更多reaction数据")
            break
        else:
            print(f"消息 {message_id} 有更多reaction，获取下一页，page_token: {page_token[:10]}...")

    return total_count


def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 获取所有message_id
    message_ids = get_message_ids()

    if not message_ids:
        print("未获取到任何message_id")
        return

    # 准备结果汇总
    total_reaction_counts = {}

    # 遍历处理每个message_id
    for message_id in message_ids:
        print(f"\n处理 message_id: {message_id}")
        # 获取该消息的所有reaction计数
        reaction_count = get_all_reactions(client, message_id)
        total_reaction_counts[message_id] = reaction_count
        print(f"message_id: {message_id}, reaction总数: {reaction_count}")

    # 输出汇总结果
    print("\n=== 汇总结果 ===")
    for message_id, count in total_reaction_counts.items():
        print(f"{message_id}: {count}个reaction")

    # 保存汇总结果到文件
    output_file = REACTION_JSON if 'REACTION_JSON' in dir() else 'reaction_summary.json'
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(total_reaction_counts, f, indent=4, ensure_ascii=False)
    print(f"\n结果已保存到 {output_file}")


if __name__ == "__main__":
    main()