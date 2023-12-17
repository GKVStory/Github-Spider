# 多维度Github项目分析软件说明文档

## 1. 项目简介

本项目旨在开发一款能够使用爬虫技术爬取GitHub网站上项目的提交记录，并进行分析的软件。通过该软件，用户可以获取特定项目的提交记录，并进行一系列的分析，以便更好地了解项目的演化过程、开发者的贡献以及项目的健康状况。

## 2.  环境配置

### 2.1 环境创建

本项目开发使用Python 3.10.9，建议使用venv创建虚拟环境

以创建名为my_venv的虚拟环境为例：

```python
# 创建环境
python -m venv my_venv
# 激活环境
.\my_venv\Scripts\activate

# (可选)使用清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2.2 安装所需库

项目开发所需要的库文件已经打包在./requirements.txt文件中，使用下面命令安装

```python
pip install -r requirements.txt
```

### 2.3 配置数据库

本项目使用Mysql数据库，版本为：

```python
MySQL Server 8.0\bin\mysql.exe  Ver 8.0.35 for Win64 on x86_64 (MySQL Community Server - GPL)
```

当前数据库基本信息为：

```python
# 设置MySQL数据库连接信息
host = 'localhost'
port = 3306
mysql_user = 'root'
password = 'rootroot'
database = 'github'
```

需要提前创建表，代码如下：

```mysql
CREATE TABLE time_series_analysis (
  weekday INT,
  commit_count INT
);
CREATE TABLE branch_management_metrics (
  branch_count INT,
  average_merge_time FLOAT
);
CREATE TABLE code_quality_metrics (
  bug_fix_count INT
);
CREATE TABLE developer_activity (
  author VARCHAR(255),
  commit_count INT,
  contribution FLOAT
);
CREATE TABLE project_metrics (
  average_frequency FLOAT
);
CREATE TABLE commit_activity (
  date DATE,
  commit_count INT
);
```

### 2.4 配置Github API认证信息

申请Github token提高爬取速率限制，从未认证时的每小时60个到认证后的5000个，申请后填入main.py的token中

## 3 项目文件功能

### 3.1 main.py

main.py代码是一个使用GitHub API和MySQL数据库的Python程序，用于分析GitHub仓库的提交活动、开发者贡献、代码质量、分支管理和时间序列，以下是代码的主要功能：

1. 导入所需的模块：`Github`用于访问GitHub API，`pymysql`用于连接MySQL数据库，`pytz`用于处理时间和时区，`datetime`和`timedelta`用于处理日期和时间间隔。
2. 设置GitHub API认证信息和MySQL数据库连接信息。
3. 获取用户输入的用户名和仓库名。
4. 使用GitHub API获取指定用户和仓库对象。
5. 连接MySQL数据库。
6. 初始化数据库。
7. 使用GitHub API获取仓库的提交记录，并将返回的`PaginatedList`转换为`List`。
8. 统计每个项目的提交数量和提交频率，保存到`commit_counts`字典中。
9. 计算平均提交频率。
10. 将提交数量和提交频率保存到MySQL数据库的`commit_activity`和`project_metrics`表中。
11. 统计每个开发者的提交数量和贡献度，保存到`developer_commits`和`developer_contributions`字典中。
12. 将开发者的提交数量和贡献度保存到MySQL数据库的`developer_activity`表中。
13. 通过提交信息分析代码质量变化趋势，统计Bug修复的数量。
14. 将Bug修复数量保存到MySQL数据库的`code_quality_metrics`表中。
15. 使用GitHub API获取仓库的分支列表，并将返回的`PaginatedList`转换为`List`。
16. 统计分支数量。
17. 使用GitHub API获取最近一周的合并请求列表。
18. 统计合并请求数量和平均合并请求处理时长。
19. 将分支数量和平均合并请求处理时长保存到MySQL数据库的`branch_management_metrics`表中。
20. 进行时间序列分析，统计每周的提交数量。
21. 将每周提交数量保存到MySQL数据库的`time_series_analysis`表中。
22. 关闭数据库连接。

### 3.2 vision.py

vision.py连接到一个MySQL数据库，并使用pymysql库执行一系列查询和数据分析操作，以下是代码的主要功能：

1. 导入所需的库：pymysql、matplotlib.pyplot和timedelta。
2. 连接到本地MySQL数据库。
3. 通过执行SQL查询从数据库中检索提交活动数据，并将日期和提交数量存储在相应的列表中。
4. 使用matplotlib.pyplot库绘制提交数量的时间序列图。
5. 从数据库中检索平均提交频率，并打印输出结果。
6. 通过执行SQL查询从数据库中检索开发者活动数据，并将作者、提交数量和贡献度存储在相应的列表中。
7. 使用matplotlib.pyplot库绘制开发者活动的条形图。
8. 打印每个作者的贡献度百分比。
9. 从数据库中检索代码质量指标-错误修复数量，并打印输出结果。
10. 从数据库中检索分支管理指标-分支数量和平均合并时间，并打印输出结果。
11. 将平均合并时间转换为datetime.timedelta对象，并打印输出秒数。
12. 从数据库中检索时间序列分析结果-星期几和提交数量，并将其存储在相应的列表中。
13. 使用matplotlib.pyplot库绘制时间序列分析的条形图。
14. 关闭数据库连接。
15. 