from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from feature.models import Recent
from timedtask.utils import generate_user_weekly_report
from user.models import User


# Create your views here.
def generate_weekly_reports():
    # 为每个用户调用生成周报
    users = User.objects.all()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    print(f"生成{start_date}至{end_date}的周报")
    # 创建一个文件存储周报
    with open('weekly_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"生成{start_date}至{end_date}的周报\n")
    for user in users:
        res = generate_user_weekly_report(user, start_date, end_date)
        # 将周报写入文件
        with open('weekly_report.txt', 'a', encoding='utf-8') as f:
            f.write(str(res) + '\n')

    print("周报生成完毕")

    # 清空recent表中w_play_count数据
    Recent.objects.all().update(w_play_count=0)


# 实例化调度器
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

# 将任务添加到调度器
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.add_job(generate_weekly_reports, 'cron', day_of_week='sun', hour=0, minute=0, id='week_report',
                  replace_existing=True)  # 在每周日午夜执行

# 启动调度器
scheduler.start()
