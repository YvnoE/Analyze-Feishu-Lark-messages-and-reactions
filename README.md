# 飞书话题群消息分析工具 / Feishu Topic Group Message Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

一个基于飞书开放平台 API 的消息分析工具 | A message analysis tool based on Feishu (Lark) Open Platform API

[中文](#中文) | [English](#english)

---

## 中文

### 项目简介

本项目是一个基于飞书开放平台 API 的消息分析工具，用于分析飞书话题群中的消息互动情况。通过获取历史消息和表情回复数据，统计每条消息的点赞数，帮助快速识别热门话题和高质量内容。

### 功能特性

- **历史消息获取**：通过飞书 API 获取指定时间范围内的群聊消息记录
- **表情统计**：统计每条消息收到的表情回复（点赞/reaction）总数
- **数据导出**：将分析结果导出为 CSV 和 JSON 格式，便于进一步分析
- **Top 内容识别**：根据表情数排序，快速找出最受欢迎的内容

### 使用场景

- 话题群运营：分析哪些话题更受欢迎
- 内容质量评估：通过互动数据评估内容质量
- 社区活跃度监测：了解群组互动趋势
- 优质内容筛选：快速找出高赞内容

### 环境要求

- Python 3.7+
- 飞书开放平台应用（需要获取 App ID 和 App Secret）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/YvnoE/Feishu-Lark-RPA.git
cd Feishu-Lark-RPA
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置飞书应用**
   - 前往 [飞书开放平台](https://open.feishu.cn/) 创建应用
   - 获取应用的 `App ID` 和 `App Secret`
   - 在应用权限中开启以下权限：
     - `im:message:readonly` - 读取消息
     - `im:message.reaction:readonly` - 读取消息表情回复
   - 将应用添加到目标群聊中

4. **创建配置文件**
```bash
# 复制配置示例文件
cp config.example.py config.py

# 编辑 config.py 填入你的配置信息
```

### 使用方法

#### 第一步：获取历史消息

编辑 `config.py` 文件，填入以下信息：
```python
APP_ID = "your_app_id"  # 替换为你的 App ID
APP_SECRET = "your_app_secret"  # 替换为你的 App Secret
CONTAINER_ID = "oc_xxxxxx"  # 替换为目标群聊的 ID
START_TIME = "1701388800"  # Unix 时间戳（10位）
END_TIME = "1704067199"  # Unix 时间戳（10位）
```

运行脚本获取历史消息：
```bash
python history.py > history.txt
```

#### 第二步：提取消息 ID 和时间

运行脚本提取信息：
```bash
python analysis.py
# 或指定文件路径
python analysis.py history.txt output.csv
```

生成的 `output.csv` 包含两列：
- `message_id`: 消息 ID
- `create_time`: 消息创建时间

#### 第三步：统计表情回复

运行脚本统计表情：
```bash
python reactions.py
```

生成的 `reaction_summary.json` 包含每条消息的表情总数，格式如下：
```json
{
    "om_xxx": 15,
    "om_yyy": 8,
    "om_zzz": 23
}
```

### 文件说明

| 文件名 | 功能描述 |
|--------|---------|
| `history.py` | 获取飞书群聊历史消息，输出到控制台/文件 |
| `analysis.py` | 解析历史消息文本，提取 message_id 和 create_time |
| `reactions.py` | 根据 message_id 获取表情回复，统计每条消息的 reaction 总数 |
| `config.py` | 配置文件（需要从 config.example.py 复制并填入真实配置） |
| `history.txt` | 历史消息原始数据（第一步输出） |
| `output.csv` | 提取的消息 ID 和时间（第二步输出） |
| `reaction_summary.json` | 消息表情统计结果（第三步输出） |

### 获取群聊 ID 和时间戳

**获取群聊 ID：**
1. 在飞书客户端打开目标群聊
2. 点击右上角设置 → 群组信息
3. 群聊 ID 会显示在页面中（以 `oc_` 开头）

**生成 Unix 时间戳：**
- 使用在线工具：[Unix Timestamp Converter](https://www.unixtimestamp.com/)
- 或使用 Python：
```python
import time
from datetime import datetime

# 转换日期为时间戳
dt = datetime(2024, 12, 1, 0, 0, 0)
timestamp = int(dt.timestamp())
print(timestamp)  # 输出10位时间戳
```

### API 参考

本项目使用的飞书开放平台 API：

1. [获取会话历史消息](https://open.feishu.cn/document/server-docs/im-v1/message/list)
2. [获取消息表情回复](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/list)

### 注意事项

- 请确保应用已被添加到目标群聊中
- API 调用受飞书开放平台频率限制，请合理设置时间范围
- 本项目目前仅包含后端脚本，暂无前端界面
- 请妥善保管 App ID 和 App Secret，不要提交到公开仓库
- 已创建 `.gitignore` 文件保护敏感配置，`config.py` 不会被提交到版本控制

### 未来计划

- [ ] 添加图形化前端界面
- [ ] 支持多群聊批量分析
- [ ] 增加数据可视化功能（柱状图、趋势图）
- [ ] 支持按表情类型分类统计
- [ ] 添加配置文件管理
- [ ] 优化 API 调用效率

### 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 联系方式

如有问题或建议，欢迎提交 [Issue](https://github.com/YvnoE/Feishu-Lark-RPA/issues)

---

## English

### Introduction

A message analysis tool based on Feishu (Lark) Open Platform API, designed to analyze message interactions in Feishu topic groups. By retrieving historical messages and emoji reaction data, it counts the number of reactions for each message, helping to quickly identify popular topics and high-quality content.

### Features

- **Historical Message Retrieval**: Fetch chat messages within a specified time range via Feishu API
- **Emoji Statistics**: Count the total number of emoji reactions for each message
- **Data Export**: Export analysis results to CSV and JSON formats for further analysis
- **Top Content Identification**: Sort by reaction count to quickly find the most popular content

### Use Cases

- Topic group operations: Analyze which topics are more popular
- Content quality assessment: Evaluate content quality through interaction data
- Community activity monitoring: Understand group interaction trends
- Quality content filtering: Quickly find highly-liked content

### Requirements

- Python 3.7+
- Feishu Open Platform application (App ID and App Secret required)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YvnoE/Feishu-Lark-RPA.git
cd Feishu-Lark-RPA
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Feishu Application**
   - Visit [Feishu Open Platform](https://open.feishu.cn/) to create an application
   - Obtain the `App ID` and `App Secret`
   - Enable the following permissions in application settings:
     - `im:message:readonly` - Read messages
     - `im:message.reaction:readonly` - Read message reactions
   - Add the application to your target chat group

4. **Create configuration file**
```bash
# Copy the example configuration file
cp config.example.py config.py

# Edit config.py and fill in your credentials
```

### Usage

#### Step 1: Retrieve Historical Messages

Edit `config.py` and fill in the following information:
```python
APP_ID = "your_app_id"  # Replace with your App ID
APP_SECRET = "your_app_secret"  # Replace with your App Secret
CONTAINER_ID = "oc_xxxxxx"  # Replace with target chat ID
START_TIME = "1701388800"  # Unix timestamp (10 digits)
END_TIME = "1704067199"  # Unix timestamp (10 digits)
```

Run the script to fetch historical messages:
```bash
python history.py > history.txt
```

#### Step 2: Extract Message IDs and Timestamps

Run the script to extract information:
```bash
python analysis.py
# Or specify file paths
python analysis.py history.txt output.csv
```

The generated `output.csv` contains two columns:
- `message_id`: Message ID
- `create_time`: Message creation time

#### Step 3: Count Emoji Reactions

Run the script to count reactions:
```bash
python reactions.py
```

The generated `reaction_summary.json` contains the total reaction count for each message:
```json
{
    "om_xxx": 15,
    "om_yyy": 8,
    "om_zzz": 23
}
```

### File Descriptions

| File | Description |
|------|-------------|
| `history.py` | Retrieve Feishu chat history, output to console/file |
| `analysis.py` | Parse history text, extract message_id and create_time |
| `reactions.py` | Fetch emoji reactions by message_id, count total reactions |
| `config.py` | Configuration file (copy from config.example.py and fill in your credentials) |
| `history.txt` | Raw historical message data (Step 1 output) |
| `output.csv` | Extracted message IDs and timestamps (Step 2 output) |
| `reaction_summary.json` | Message reaction statistics (Step 3 output) |

### Getting Chat ID and Timestamps

**Get Chat ID:**
1. Open the target chat in Feishu client
2. Click settings in upper right → Group Info
3. Chat ID will be displayed (starts with `oc_`)

**Generate Unix Timestamp:**
- Use online tool: [Unix Timestamp Converter](https://www.unixtimestamp.com/)
- Or use Python:
```python
import time
from datetime import datetime

# Convert date to timestamp
dt = datetime(2024, 12, 1, 0, 0, 0)
timestamp = int(dt.timestamp())
print(timestamp)  # Output 10-digit timestamp
```

### API Reference

Feishu Open Platform APIs used in this project:

1. [Get Chat History](https://open.feishu.cn/document/server-docs/im-v1/message/list)
2. [Get Message Reactions](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/list)

### Notes

- Ensure the application has been added to the target chat
- API calls are subject to Feishu Open Platform rate limits
- This project currently only includes backend scripts without a frontend interface
- Keep your App ID and App Secret secure, do not commit them to public repositories
- `.gitignore` file is configured to protect sensitive configurations, `config.py` will not be committed to version control

### Roadmap

- [ ] Add graphical frontend interface
- [ ] Support batch analysis for multiple chats
- [ ] Add data visualization (bar charts, trend graphs)
- [ ] Support reaction statistics by emoji type
- [ ] Add configuration file management
- [ ] Optimize API call efficiency

### Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

### Contact

For questions or suggestions, please submit an [Issue](https://github.com/YvnoE/Feishu-Lark-RPA/issues)
