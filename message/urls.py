from django.urls import path
from . import views

urlpatterns = [
    # 测试接口
    path('test/', views.test),
]
