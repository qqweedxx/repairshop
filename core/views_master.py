from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderStatusHistory, Comment, OrderPart, Part
from .forms import StatusChangeForm, CommentForm, OrderPartForm, OrderCostForm
from .decorators import role_required


@role_required('master', 'admin')
def master_dashboard(request):
    if request.user.role == 'admin':
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(master=request.user).order_by('-created_at')
        
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    return render(request, 'master_dashboard.html', {'orders': orders})


@role_required('master', 'admin')
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.role == 'master' and order.master != request.user:
        messages.error(request, 'Это не ваша заявка.')
        return redirect('master_dashboard')

    if request.method == 'POST':
        old_status = order.status
        form = StatusChangeForm(request.POST, instance=order)
        
        if form.is_valid():
            updated_order = form.save(commit=False)
            
            total_cost = request.POST.get('total_cost')
            if total_cost:
                updated_order.total_cost = total_cost
                
            updated_order.save()

            if old_status != updated_order.status:
                OrderStatusHistory.objects.create(
                    order=updated_order,
                    status=updated_order.status,
                    changed_by=request.user
                )
                messages.success(request, f'Статус изменён на «{updated_order.get_status_display()}».')

            comment_text = request.POST.get('comment', '').strip()
            if comment_text:
                Comment.objects.create(
                    order=updated_order,
                    author=request.user,
                    text=comment_text
                )
                messages.success(request, 'Комментарий добавлен.')
                
            return redirect('master_dashboard')
    else:
        form = StatusChangeForm(instance=order)

    return render(request, 'order_update_status.html', {
        'form': form,
        'order': order,
    })

@role_required('master', 'admin')
def order_add_comment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.role == 'master' and order.master != request.user:
        messages.error(request, 'Это не ваша заявка.')
        return redirect('master_dashboard')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.order = order
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('master_dashboard')

    return render(request, 'order_add_comment.html', {
        'form': CommentForm(),
        'order': order,
    })

@role_required('master', 'admin')
def order_add_part(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.role == 'master' and order.master != request.user:
        messages.error(request, 'Это не ваша заявка.')
        return redirect('master_dashboard')

    if request.method == 'POST':
        form = OrderPartForm(request.POST)
        if form.is_valid():
            order_part = form.save(commit=False)
            order_part.order = order
            
            part = order_part.part
            if part.quantity_in_stock >= order_part.quantity_used:
                part.quantity_in_stock -= order_part.quantity_used
                part.save()
                order_part.save() 
                messages.success(request, f'Запчасть «{part.name}» добавлена, остаток на складе: {part.quantity_in_stock}.')
            else:
                messages.error(request, f'Ошибка! На складе только {part.quantity_in_stock} шт. запчасти «{part.name}».')
            return redirect('master_dashboard')
    else:
        form = OrderPartForm()

    return render(request, 'order_add_part.html', {'form': form, 'order': order})


@role_required('master', 'admin')
def order_update_cost(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.role == 'master' and order.master != request.user:
        messages.error(request, 'Это не ваша заявка.')
        return redirect('master_dashboard')

    if request.method == 'POST':
        form = OrderCostForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Стоимость работ обновлена.')
            return redirect('master_dashboard')
    else:
        form = OrderCostForm(instance=order)

    return render(request, 'order_update_cost.html', {'form': form, 'order': order})