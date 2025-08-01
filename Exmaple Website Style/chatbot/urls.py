from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('api/message/', views.send_message, name='send_message'),
    path('api/session/', views.get_or_create_session, name='get_or_create_session'),
    path('api/history/<uuid:session_id>/', views.get_chat_history, name='get_chat_history'),
]