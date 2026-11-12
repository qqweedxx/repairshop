from django.urls import path
from . import views
from . import views_client
from . import views_master

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
        path('orders/create/', views_client.order_create, name='order_create'),
            path('my-orders/', views_client.client_dashboard, name='client_dashboard'),
                path('master/', views_master.master_dashboard, name='master_dashboard'),
    path('master/order/<int:order_id>/status/', views_master.order_update_status, name='order_update_status'),
    path('master/order/<int:order_id>/comment/', views_master.order_add_comment, name='order_add_comment'),
]