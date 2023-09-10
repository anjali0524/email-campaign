from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='my-view'),
    path('add_subscriber/', views.add_subscriber, name='add_subscriber'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('send_campaign/', views.send_campaign, name='send_campaign'),
    path('test_send_campaign_email/', views.test_send_campaign_email, name='test_send_campaign_email'),
]
