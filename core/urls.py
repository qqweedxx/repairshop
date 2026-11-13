from django.urls import path
from . import views
from . import views_client
from . import views_master
from . import views_admin

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
        
    path('stats/', views_admin.stats_page, name='stats_page'),
    path('api/stats/orders/', views_admin.stats_orders_by_period, name='api_stats_orders'),
    path('api/stats/revenue/', views_admin.stats_revenue, name='api_stats_revenue'),
    path('api/stats/services/', views_admin.stats_popular_services, name='api_stats_services'),
    path('api/stats/masters/', views_admin.stats_masters_load, name='api_stats_masters'),
    path('master/order/<int:order_id>/part/', views_master.order_add_part, name='order_add_part'),
    path('master/order/<int:order_id>/cost/', views_master.order_update_cost, name='order_update_cost'),
]