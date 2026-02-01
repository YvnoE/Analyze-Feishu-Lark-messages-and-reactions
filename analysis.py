import re
import csv
import sys
import os
from typing import List, Dict, Tuple


def extract_message_info(text: str) -> List[Dict[str, str]]:
    """
    从文本中提取message_id和create_time字段

    参数:
    text (str): 包含JSON响应的文本

    返回:
    List[Dict[str, str]]: 提取的信息列表，每个元素是包含message_id和create_time的字典
    """
    # 定义正则表达式模式
    # 匹配message_id和create_time字段，考虑它们可能的顺序不同
    pattern = re.compile(r'"message_id":\s*"([^"]+)"|"create_time":\s*"([^"]+)"')

    # 用于存储提取结果的列表
    results = []
    current_item = {}

    # 查找所有匹配项
    matches = pattern.finditer(text)

    for match in matches:
        if match.group(1):  # 匹配到message_id
            current_item["message_id"] = match.group(1)
        elif match.group(2):  # 匹配到create_time
            current_item["create_time"] = match.group(2)

        # 当同时找到message_id和create_time时，将其添加到结果列表并重置当前项
        if "message_id" in current_item and "create_time" in current_item:
            results.append(current_item.copy())
            current_item = {}

    return results


def process_log_file(file_path: str) -> List[Dict[str, str]]:
    """
    处理日志文件，提取所有message_id和create_time

    参数:
    file_path (str): 日志文件路径

    返回:
    List[Dict[str, str]]: 提取的信息列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return extract_message_info(content)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []


def save_to_csv(data: List[Dict[str, str]], output_file: str) -> None:
    """
    将提取的数据保存为CSV文件

    参数:
    data (List[Dict[str, str]]): 提取的数据
    output_file (str): 输出CSV文件路径
    """
    if not data:
        print("没有数据可保存")
        return

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['message_id', 'create_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)

        print(f"数据已成功保存到 {output_file}")
    except Exception as e:
        print(f"保存CSV文件时发生错误: {e}")


def main():
    """主函数"""
    # 尝试从配置文件读取文件名
    try:
        from config import HISTORY_FILE, OUTPUT_CSV
        input_file = HISTORY_FILE
        output_file = OUTPUT_CSV
    except ImportError:
        # 如果配置文件不存在，使用默认值
        input_file = 'history.txt'
        output_file = 'output.csv'

    # 检查默认输入文件是否存在
    if not os.path.exists(input_file):
        print(f"警告: 默认文件 '{input_file}' 不存在")
        print("请先运行 history.py 生成历史消息文件")
        print("或通过命令行参数指定其他文件路径")

    # 处理命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"正在处理文件: {input_file}")
    messages = process_log_file(input_file)

    print(f"共提取出 {len(messages)} 条记录")

    if messages:
        save_to_csv(messages, output_file)


if __name__ == "__main__":
    main()