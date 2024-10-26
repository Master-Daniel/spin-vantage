"""
APP's local routes
"""
from django.urls import path

from . import views

app_name = 'wheel'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('forgot-password', views.forgottenPassword, name='forgot-password'),
    path('how-to-play', views.howToPlay, name='how-to-play'),
    path('logout', views.logout, name='logout'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.terms, name='privacy'),
    path('contact-us', views.contactus, name='contact-us'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('draw', views.draw_spin, name='draw_spin'),
    path('<int:pk>', views.draw_result, name='draw_result'),
]
