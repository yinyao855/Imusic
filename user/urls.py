from django.urls import path
from . import views

urlpatterns = [
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('info/<str:username>', views.get_user_info, name='info'),
    path('update/<str:username>', views.update_user_info, name='update'),
    path('delete/<str:username>', views.delete_user, name='delete'),

]
