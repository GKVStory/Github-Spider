import remi.gui as gui
from remi import start, App
from github import Github
import pymysql, pytz
from datetime import datetime, timedelta
import os
from github import Github
import pymysql, pytz
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from datetime import timedelta
import warnings, os
import matplotlib

matplotlib.use('Agg')

warnings.filterwarnings("ignore", category=UserWarning)

class MyApp(App):
    def __init__(self, *args):
        #super(MyApp, self).__init__(*args)
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
        #print(res_path)
        #declare here resource folders as a dictionary, the parameter is *static_file_path*
        super(MyApp, self).__init__(*args, static_file_path={'my_res_folder':res_path})

    def main(self):
        
        # token = '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'
        token = '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'
        self.g = Github(token)
        self.wid = gui.VBox(width='80%', height='80%')
        
        
        self.lbl = gui.Label('input github user name', width=300, height=100, margin = '13px', style={"white-space":"pre"})
        self.text = gui.TextInput(width=300, margin = '13px')
        self.img = gui.Image('/my_res_folder:ruangong.jpg', width=300, margin = '13px')

        
        #一个简单交互的按钮
        self.bt = gui.Button('enter!', width=200, height=30)

        #建立这个按钮的点击事件
        self.bt.onclick.do(self.on_button_pressed)

        #添加按钮到容器
        self.wid.append(self.img)
        self.wid.append(self.lbl)
        self.wid.append(self.text)
        self.wid.append(self.bt)
        # 返回根部件
        return self.wid

    # 按钮的点击事件
    def on_button_pressed(self, emitter):
        #self.lbl.set_text('please select the repo you are intrested ')
        #self.bt.set_text('alread pressed')
        self.wid.remove_child(self.bt)
        self.wid.remove_child(self.img)
        self.wid.remove_child(self.text)
        #print(self.user_name.get_text())
        user_input = self.text.get_text()
        try:
            user = self.g.get_user(user_input)
        except:
            self.lbl.set_text('you input the wrong username ')
            return
        self.username = user_input
        self.lbl.set_text('please select the repo you are intrested from ' + user_input)
        
        #repository_input = "Python"
        repolist = []
        
        i = 0
        wid1 = gui.VBox(width='100%', height='30%')
        wid2 = gui.VBox(width='100%', height='30%')
        wid3 = gui.VBox(width='100%', height='30%')
        hwid = gui.HBox(width='100%', height='70%')
        for repo in user.get_repos():
            if i % 3 == 0:
                repolist.append(repo.name)
                wid1.append(gui.Button(repo.name, width=200, height=30), repo.name)
                #print(wid1.children[repo.name])
                wid1.children[repo.name].onclick.do(self.showdata, repo.name)
            elif i % 3 == 1:
                wid2.append(gui.Button(repo.name, width=200, height=30), repo.name)
                wid2.children[repo.name].onclick.do(self.showdata, repo.name)
                repolist.append(repo.name)
            else :
                wid3.append(gui.Button(repo.name, width=200, height=30), repo.name)
                wid3.children[repo.name].onclick.do(self.showdata, repo.name)
                repolist.append(repo.name)
            i += 1
        hwid.append([wid1,wid2,wid3])
        self.wid.append(hwid)
        print(user)
        print(repolist)

    def showdata(self,emitter, repo_name):# 在这个函数里利用self.user_name and repo_name 把数据存进数据库里并进行展示
        user_name = self.username
        repo_name = repo_name

        # 设置Github API认证信息
        token = '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'
        g = Github(token)

        # 设置MySQL数据库连接信息
        host = 'localhost'
        port = 3306
        mysql_user = 'root'
        password = 'rootroot'
        database = 'github'

        user_input = user_name
        repository_input = repo_name

        # 获取指定用户和仓库对象
        user = g.get_user(user_input)
        repo = user.get_repo(repository_input)

        print(type(user), repo)

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
            date = commit.commit.author.date.date()  # 提交日期
            if date not in commit_counts:
                commit_counts[date] = 0
            commit_counts[date] += 1

        # 计算平均提交频率
        total_days = (datetime.now().date() - min(commit_counts.keys())).days + 1
        average_frequency = len(commits) / total_days

        # 保存提交数量和提交频率到数据库
        with connection.cursor() as cursor:
            for date, count in commit_counts.items():
                sql = "INSERT INTO `commit_activity` (`date`, `commit_count`) VALUES (%s, %s)"
                cursor.execute(sql, (date, count))

            sql = "INSERT INTO `project_metrics` (`average_frequency`) VALUES (%s)"
            cursor.execute(sql, (average_frequency,))

        connection.commit()

        # 统计每个开发者的提交数量和贡献度
        developer_commits = {}
        total_commits = len(commits)
        for commit in commits:
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

        # 通过提交信息分析代码质量变化趋势
        bug_keywords = ['bug', 'fix']  # 定义关键词列表
        bug_fix_count = 0
        for commit in commits:
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

        # 保存分支数量和平均合并请求处理时长到数据库
        with connection.cursor() as cursor:
            sql = "INSERT INTO `branch_management_metrics` (`branch_count`, `average_merge_time`) VALUES (%s, %s)"
            cursor.execute(sql, (branch_count, average_merge_time.total_seconds()))

        connection.commit()

        # 时间序列分析
        weekday_commit_counts = {i: 0 for i in range(7)}  # 初始化每周的提交数量为0
        for commit in commits:
            weekday = commit.commit.author.date.weekday()
            weekday_commit_counts[weekday] += 1

        # 保存每周提交数量到数据库
        with connection.cursor() as cursor:
            for weekday, count in weekday_commit_counts.items():
                sql = "INSERT INTO `time_series_analysis` (`weekday`, `commit_count`) VALUES (%s, %s)"
                cursor.execute(sql, (weekday, count))

        connection.commit()

        # 关闭数据库连接
        connection.close()


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
        plt.close()

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
        plt.close()

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
        plt.close()

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




        dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page')
        self.dlbl_user = gui.Label()
        self.dlbl_repo = gui.Label()
        self.dlbl_user.set_text(user_name)
        self.dlbl_repo.set_text(repo_name)
        dialog.add_field('user_name',self.dlbl_user)
        dialog.add_field('repo_name',self.dlbl_repo)
        dimg1 = gui.Image('/my_res_folder:commit_activity.png')
        #dimg1.set_image('/my_res_folder:commit_activity.png')
        dialog.add_field_with_label('dimg1', 'commit_activiy', dimg1)
        dimg2 = gui.Image('/my_res_folder:developer_activity.png')
        dialog.add_field_with_label('dimg2', 'developer_activity', dimg2)
        dimg3 = gui.Image('/my_res_folder:time_series_analysis.png')
        dialog.add_field_with_label('dimg3', 'time_series_analysis', dimg3)

        #self.dialog.confirm_dialog.do(self.dialog_confirm)
        dialog.show(self)
        


if __name__ == "__main__":
    # 开启服务器，在IP0.0.0.0,端口为随机
    start(MyApp, debug=True, address='0.0.0.0', port=0)
