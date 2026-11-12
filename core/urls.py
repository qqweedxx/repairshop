from django.urls import path
from . import views
from . import views_client

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
        path('orders/create/', views_client.order_create, name='order_create'),
]