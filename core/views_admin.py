from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Order, Service, User
from .decorators import role_required
from django.contrib import messages


@role_required('admin', 'master')
def stats_page(request):
    new_orders = Order.objects.filter(status='accepted').count()
    
    in_progress = Order.objects.exclude(status__in=['ready', 'issued']).count()
    
    total_revenue = Order.objects.filter(status='issued').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    context = {
        'total_orders': new_orders,
        'in_progress': in_progress,
        'total_revenue': int(total_revenue),
    }
    return render(request, 'stats.html', context)

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

@role_required('admin')
def admin_dashboard(request):
    """Страница распределения заявок"""
    orders = Order.objects.all().order_by('-created_at')
    masters = User.objects.filter(role='master')
    return render(request, 'admin_dashboard.html', {'orders': orders, 'masters': masters})

@role_required('admin')
def assign_master(request, order_id):
    """Назначение мастера на заявку"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        master_id = request.POST.get('master_id')
        
        if master_id:
            master = get_object_or_404(User, id=master_id, role='master')
            order.master = master
            order.save()
            messages.success(request, f'Мастер {master.username} назначен на заявку #{order.id}.')
        else:
            order.master = None 
            order.save()
            messages.info(request, f'С заявки #{order.id} снят мастер.')
            
    return redirect('admin_dashboard')