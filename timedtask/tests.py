import os
from unittest.mock import patch, mock_open
from django.test import TestCase
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from song.models import Song
from timedtask.views import generate_weekly_reports
from user.models import User
from feature.models import Recent


class GenerateWeeklyReportsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password1'
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password2'
        )
        self.recent1 = Recent.objects.create(
            song=Song.objects.filter(id=5).first(),
            user=self.user1,
            w_play_count=10
        )
        self.recent2 = Recent.objects.create(
            song=Song.objects.filter(id=5).first(),
            user=self.user2,
            w_play_count=20
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('timedtask.views.generate_user_weekly_report')
    @patch('timedtask.views.generate_user_upload_weekly_report')
    def test_generate_weekly_reports(self, mock_generate_user_upload_weekly_report, mock_generate_user_weekly_report, mock_open_file):
        mock_generate_user_weekly_report.side_effect = lambda user, start_date, end_date: f"Weekly report for {user.username}"
        mock_generate_user_upload_weekly_report.side_effect = lambda user, start_date, end_date: f"Upload report for {user.username}"

        generate_weekly_reports()

        # 验证文件写入
        mock_open_file.assert_called_with('weekly_report.txt', 'a', encoding='utf-8')
        handle = mock_open_file()
        handle.write.assert_any_call(f"Weekly report for user1\n")
        handle.write.assert_any_call(f"Upload report for user1\n")
        handle.write.assert_any_call(f"Weekly report for user2\n")
        handle.write.assert_any_call(f"Upload report for user2\n")

        # 验证Recent表w_play_count字段重置
        self.recent1.refresh_from_db()
        self.recent2.refresh_from_db()
        self.assertEqual(self.recent1.w_play_count, 0)
        self.assertEqual(self.recent2.w_play_count, 0)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.recent1.delete()
        self.recent2.delete()
        os.remove('weekly_report.txt')


class SchedulerTests(TestCase):
    @patch('timedtask.views.generate_weekly_reports')
    def test_scheduler(self, mock_generate_weekly_reports):
        scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(generate_weekly_reports, 'cron', day_of_week='sun', hour=0, minute=0, id='week_report',
                          replace_existing=True)
        scheduler.start()
        job = scheduler.get_job('week_report')
        self.assertIsNotNone(job)
        self.assertEqual(job.id, 'week_report')
        scheduler.shutdown()

