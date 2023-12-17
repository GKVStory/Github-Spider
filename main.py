from github import Github
import pymysql, pytz
from datetime import datetime, timedelta

# 设置Github API认证信息
token = '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'
g = Github(token)

# 设置MySQL数据库连接信息
host = 'localhost'
port = 3306
mysql_user = 'root'
password = 'rootroot'
database = 'github'

user_input = input("请输入用户名：")
repository_input = input("请输入仓库名：")

# 获取指定用户和仓库对象
user = g.get_user(user_input)
repo = user.get_repo(repository_input)

print("Processing User: %s with Repo: %s" %(user, repo))

# 连接MySQL数据库
connection = pymysql.connect(host=host, port=port, user=mysql_user, password=password, database=database, charset='utf8mb4')

# 初始化数据库
cursor = connection.cursor()
cursor.execute("TRUNCATE TABLE `commit_activity`")
cursor.execute("TRUNCATE TABLE `project_metrics`")
cursor.execute("TRUNCATE TABLE `developer_activity`")
cursor.execute("TRUNCATE TABLE `code_quality_metrics`")
cursor.execute("TRUNCATE TABLE `branch_management_metrics`")
cursor.execute("TRUNCATE TABLE `time_series_analysis`")


# 获取commit记录，将PaginatedList转换为List
commits = list(repo.get_commits())

# 统计每个项目的提交数量和提交频率
commit_counts = {}
for commit in commits:
    # print("Processing Commit: %s" %commit)
    date = commit.commit.author.date.date()  # 提交日期
    if date not in commit_counts:
        commit_counts[date] = 0
    commit_counts[date] += 1

# 计算平均提交频率
total_days = (datetime.now().date() - min(commit_counts.keys())).days + 1
average_frequency = len(commits) / total_days

print("Calcuate done, the average frequency is %s" %average_frequency)

# 保存提交数量和提交频率到数据库
with connection.cursor() as cursor:
    for date, count in commit_counts.items():
        sql = "INSERT INTO `commit_activity` (`date`, `commit_count`) VALUES (%s, %s)"
        cursor.execute(sql, (date, count))

    sql = "INSERT INTO `project_metrics` (`average_frequency`) VALUES (%s)"
    cursor.execute(sql, (average_frequency,))

connection.commit()

print("Update commit count and average frequency complete")

# 统计每个开发者的提交数量和贡献度
developer_commits = {}
total_commits = len(commits)
for commit in commits:
    # print("Processing Commit: %s" %commit)
    author = commit.commit.author.name
    if author not in developer_commits:
        developer_commits[author] = 0
    developer_commits[author] += 1

# 计算每个开发者的贡献度
developer_contributions = {author: count / total_commits for author, count in developer_commits.items()}


# 保存开发者提交数量和贡献度到数据库
with connection.cursor() as cursor:
    for author, count in developer_commits.items():
        sql = "INSERT INTO `developer_activity` (`author`, `commit_count`, `contribution`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (author, count, developer_contributions[author]))

connection.commit()

print("Update author, commit_count and contribution complete, conclude %d times commit" %total_commits)

# 通过提交信息分析代码质量变化趋势
bug_keywords = ['bug', 'fix']  # 定义关键词列表
bug_fix_count = 0
for commit in commits:
    # print("Processing Commit: %s" %commit)
    message = commit.commit.message.lower()
    for keyword in bug_keywords:
        if keyword in message:
            bug_fix_count += 1
            break

# 保存Bug修复数量到数据库
with connection.cursor() as cursor:
    sql = "INSERT INTO `code_quality_metrics` (`bug_fix_count`) VALUES (%s)"
    cursor.execute(sql, (bug_fix_count))

connection.commit()

print("Update bug fix count complete, the result is %d" %bug_fix_count)

# 分支管理分析，将PaginatedList转换为List
branches = list(repo.get_branches())
branch_count = len(branches)

# 获取最近一周的合并请求
week_ago = datetime.now(pytz.utc) - timedelta(days=7)
pull_requests = [pr for pr in repo.get_pulls(state='closed', sort='updated', direction='desc', base='master') if pr.created_at >= week_ago]


pull_request_count = 0
average_merge_time = timedelta()
for pr in pull_requests:
    pull_request_count += 1
    created_at = pr.created_at
    merged_at = pr.merged_at
    if merged_at:
        merge_time = merged_at - created_at
        average_merge_time += merge_time

# 计算平均合并请求处理时长
average_merge_time = average_merge_time / pull_request_count if pull_request_count > 0 else timedelta()
print("Calcuate average merge time done, the result is %s" %average_merge_time)

# 保存分支数量和平均合并请求处理时长到数据库
with connection.cursor() as cursor:
    sql = "INSERT INTO `branch_management_metrics` (`branch_count`, `average_merge_time`) VALUES (%s, %s)"
    cursor.execute(sql, (branch_count, average_merge_time.total_seconds()))

connection.commit()

print("Update branch count and average merge time complete, conclude %d branches" %branch_count)

# 时间序列分析
weekday_commit_counts = {i: 0 for i in range(7)}  # 初始化每周的提交数量为0
for commit in commits:
    # print("Processing Commit: %s" %commit)
    weekday = commit.commit.author.date.weekday()
    weekday_commit_counts[weekday] += 1

# 保存每周提交数量到数据库
with connection.cursor() as cursor:
    for weekday, count in weekday_commit_counts.items():
        sql = "INSERT INTO `time_series_analysis` (`weekday`, `commit_count`) VALUES (%s, %s)"
        cursor.execute(sql, (weekday, count))

connection.commit()
print("Update weekday and commit count time complete")

# 关闭数据库连接
connection.close()
print("Update all database complete")
