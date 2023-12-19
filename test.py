import requests


# 指定owner和repo
owner = "facebookresearch"
repo = "llama"

# 构建API请求URL
url = f"https://api.github.com/repos/{owner}/{repo}/commits"

# 使用GitHub API获取COMMIT数据
response = requests.get(url)

# 解析COMMIT数据
commits = response.json()
# print(commits)

author_commits = {}

# 统计每个作者的提交数量
for commit in commits:
    author = commit['commit']['author']['name']
    if author in author_commits:
        author_commits[author] += 1
    else:
        author_commits[author] = 1

# 打印每个作者的提交数量
for author, commit_count in author_commits.items():
    print(f'{author}: {commit_count} commits')
