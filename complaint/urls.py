from django.urls import path, include
from complaint import views


urlpatterns = [
    # 管理员查看投诉内容
    path('review', views.get_complaint, name='get_complaint'),
    # 管理员处理审查
    path('handle', views.handle_complaint, name='handle_complaint'),
    # 管理员审查并确定下架后，被投诉者可以申诉
    path('appeal', views.appeal, name='appeal'),
    # 查看申诉内容
    path('appeals/review', views.get_appeal, name='get_appeal'),
    # 管理员处理申诉
    path('appeals/handle', views.handle_appeal, name='handle_appeal'),
]
