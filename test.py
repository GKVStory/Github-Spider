import unittest
from github import Github
import pymysql, pytz
from datetime import datetime, timedelta

# 设置Github API认证信息，token最好自己用的时候去申请一个
token = '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'
g = Github(token)

# https://github.com/yangyaojia/Bilibili_video_download
user_input = "yangyaojia"
repository_input = "Bilibili_video_download"

# 获取指定用户和仓库对象
user = g.get_user(user_input)
repo = user.get_repo(repository_input)

# 获取commit记录，将PaginatedList转换为List
commits = list(repo.get_commits())

commit_counts = {}
for commit in commits:
    date = commit.commit.author.date.date()  # 提交日期
    if date not in commit_counts:
        commit_counts[date] = 0
    commit_counts[date] += 1

# 计算平均提交频率
total_days = (datetime.now().date() - min(commit_counts.keys())).days + 1
average_frequency = len(commits) / total_days

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

# 时间序列分析
weekday_commit_counts = {i: 0 for i in range(7)}  # 初始化每周的提交数量为0
for commit in commits:
    # print("Processing Commit: %s" %commit)
    weekday = commit.commit.author.date.weekday()
    weekday_commit_counts[weekday] += 1


class MyCodeTest(unittest.TestCase):
    def test_average_frequency(self):
        self.assertEqual(average_frequency, 0.03470031545741325)

    def test_total_commits(self):
        self.assertEqual(total_commits, 66)

    def test_developer_commits(self):
        self.assertEqual(developer_commits['Henryhaohao'], 53)

    def test_developer_contributions(self):
        self.assertEqual(developer_contributions['Henryhaohao'], 0.803030303030303)
    
    def test_bug_fix_count(self):
        self.assertEqual(bug_fix_count, 2)
    
    def test_branch_count(self):
        self.assertEqual(branch_count, 2)
    
    def test_average_merge_time(self):
        self.assertEqual(average_merge_time, timedelta(seconds=0))

    def test_weekday_commit_counts(self):
        self.assertEqual(weekday_commit_counts, {0: 5, 1: 10, 2: 7, 3: 10, 4: 8, 5: 16, 6: 10})

if __name__ == '__main__':
    unittest.main()
