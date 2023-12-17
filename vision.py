import pymysql
import matplotlib.pyplot as plt
from datetime import timedelta
import warnings, os

warnings.filterwarnings("ignore", category=UserWarning)


# 创建文件夹保存输出
os.makedirs('result', exist_ok=True)

# 连接MySQL数据库
connection = pymysql.connect(host='localhost', port=3306, user='root', password='rootroot', database='github', charset='utf8mb4')

# 展示每个项目的提交数量和提交频率
with connection.cursor() as cursor:
    sql = "SELECT `date`, `commit_count` FROM `commit_activity`"
    cursor.execute(sql)
    results = cursor.fetchall()
    dates = [result[0] for result in results]
    commit_counts = [result[1] for result in results]

plt.plot(dates, commit_counts)
plt.xlabel('Date')
plt.ylabel('Commit Count')
plt.title('Commit Activity')
plt.savefig('result/commit_activity.png')
plt.show()

with connection.cursor() as cursor:
    sql = "SELECT `average_frequency` FROM `project_metrics`"
    cursor.execute(sql)
    average_frequency = cursor.fetchone()[0]

# print("Average Commit Frequency: {:.2f} commits per day".format(average_frequency))

# 展示每个开发者的提交数量和贡献度，只显示3个字母
with connection.cursor() as cursor:
    sql = "SELECT `author`, `commit_count`, `contribution` FROM `developer_activity`"
    cursor.execute(sql)
    results = cursor.fetchall()
    authors = [result[0][:3] for result in results]
    commit_counts = [result[1] for result in results]
    contributions = [result[2] for result in results]

plt.bar(authors, commit_counts)
plt.xlabel('Author')
plt.ylabel('Commit Count')
plt.title('Developer Activity')
plt.savefig('result/developer_activity.png') 
plt.show()

# for author, contribution in zip(authors, contributions):
#     print("{}: {:.2%}".format(author, contribution))

# 展示代码质量变化趋势
with connection.cursor() as cursor:
    sql = "SELECT `bug_fix_count` FROM `code_quality_metrics`"
    cursor.execute(sql)
    bug_fix_count = cursor.fetchone()[0]

# print("Bug Fix Count: {}".format(bug_fix_count))

# 展示分支管理分析结果
with connection.cursor() as cursor:
    sql = "SELECT `branch_count`, `average_merge_time` FROM `branch_management_metrics`"
    cursor.execute(sql)
    result = cursor.fetchone()
    branch_count = result[0]
    average_merge_time = result[1]

# 将浮点数平均合并时间转换为datetime.timedelta对象
merge_delta = timedelta(seconds=average_merge_time)

# 调用total_seconds()方法获取秒数
seconds = merge_delta.total_seconds()

# print("Branch Count: {}".format(branch_count))
# print("Average Merge Time: {} seconds".format(seconds))

# 展示时间序列分析结果
with connection.cursor() as cursor:
    sql = "SELECT `weekday`, `commit_count` FROM `time_series_analysis`"
    cursor.execute(sql)
    results = cursor.fetchall()
    weekdays = [result[0] for result in results]
    commit_counts = [result[1] for result in results]

plt.bar(weekdays, commit_counts)
plt.xlabel('Weekday')
plt.ylabel('Commit Count')
plt.title('Time Series Analysis')
plt.savefig('result/time_series_analysis.png')
plt.show()

with open('result/output.txt', 'w') as f:
    f.write("Average Commit Frequency: {:.2f} commits per day\n".format(average_frequency))
    f.write("\n")
    f.write("Bug Fix Count: {}\n".format(bug_fix_count))
    f.write("\n")
    f.write("Branch Count: {}\n".format(branch_count))
    f.write("Average Merge Time: {} seconds\n".format(seconds))
    f.write("\n")
    f.write("Author: Contribution\n")
    for author, contribution in zip(authors, contributions):
        f.write("{}: {:.2%}\n".format(author, contribution))


# 关闭数据库连接
connection.close()
