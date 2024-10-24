"""
APP's local routes
"""
from django.urls import path

from . import views

app_name = 'wheel'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('draw', views.draw_spin, name='draw_spin'),
    path('<int:pk>', views.draw_result, name='draw_result'),
]
