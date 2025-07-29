from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.home, name='home'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('assets/download/<int:asset_id>/', views.download_asset, name='download_asset'),
    path('upload/', views.upload_asset, name='upload_asset'),
    path('category/<slug:category_slug>/', views.category_assets, name='category_assets'),
    path('search/', views.search_assets, name='search_assets'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]

