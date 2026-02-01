# 飞书应用配置示例文件 / Feishu Application Configuration Example
# 使用方法 / Usage: 复制此文件为 config.py 并填入真实配置 / Copy this file to config.py and fill in your credentials

# 飞书应用凭证 / Feishu App Credentials
APP_ID = "your_app_id_here"
APP_SECRET = "your_app_secret_here"

# 目标群聊配置 / Target Chat Configuration
CONTAINER_ID = "your_chat_id_here"  # 群聊ID，以 oc_ 开头 / Chat ID starting with oc_

# 时间范围配置 / Time Range Configuration
START_TIME = "1701388800"  # 起始时间 Unix 时间戳 / Start timestamp (10 digits)
END_TIME = "1704067199"    # 结束时间 Unix 时间戳 / End timestamp (10 digits)

# 文件配置 / File Configuration
HISTORY_FILE = "history.txt"
OUTPUT_CSV = "output.csv"
REACTION_JSON = "reaction_summary.json"
