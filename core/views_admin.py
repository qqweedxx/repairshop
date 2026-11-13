from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Order, Service
from .decorators import role_required


@role_required('admin', 'master')
def stats_page(request):
    """Страница со статистикой (шаблон stats.html сверстает напарник)"""
    return render(request, 'stats.html')


@role_required('admin', 'master')
def stats_orders_by_period(request):
    """Заявки по дням за последние 30 дней"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    data = (Order.objects
            .filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date'))
    
    result = [{'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in data]
    return JsonResponse(result, safe=False)


@role_required('admin', 'master')
def stats_revenue(request):
    """Доход по месяцам (только выданные заявки)"""
    data = (Order.objects
            .filter(status='issued')
            .annotate(month=TruncMonth('updated_at'))
            .values('month')
            .annotate(total=Sum('total_cost'))
            .order_by('month'))
            
    result = [{'month': item['month'].strftime('%Y-%m'), 'total': float(item['total'] or 0)} for item in data]
    return JsonResponse(result, safe=False)


@role_required('admin', 'master')
def stats_popular_services(request):
    """Топ-5 услуг по количеству заявок"""
    data = (Service.objects
            .annotate(order_count=Count('order'))
            .filter(order_count__gt=0)
            .order_by('-order_count')[:5]
            .values('name', 'order_count'))
            
    result = [{'name': item['name'], 'count': item['order_count']} for item in data]
    return JsonResponse(result, safe=False)


@role_required('admin', 'master')
def stats_masters_load(request):
    """Сколько заявок у каждого мастера"""
    data = (Order.objects
            .filter(master__isnull=False)
            .values('master__username')
            .annotate(count=Count('id'))
            .order_by('-count'))
            
    result = [{'master': item['master__username'], 'count': item['count']} for item in data]
    return JsonResponse(result, safe=False)