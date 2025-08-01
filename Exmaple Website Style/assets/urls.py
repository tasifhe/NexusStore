from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('create/', views.create_asset, name='create_asset'),
    path('<uuid:pk>/', views.asset_detail, name='asset_detail'),
    path('<uuid:pk>/edit/', views.edit_asset, name='edit_asset'),
    path('<uuid:pk>/delete/', views.delete_asset, name='delete_asset'),
    path('<uuid:pk>/download/', views.download_asset, name='download_asset'),
    path('<uuid:pk>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('<uuid:pk>/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<uuid:pk>/purchase/', views.purchase_asset, name='purchase_asset'),
    path('<uuid:pk>/review/', views.add_review, name='add_review'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories/', views.category_list, name='category_list'),
]