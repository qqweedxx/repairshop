from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderStatusHistory, Comment
from .forms import StatusChangeForm, CommentForm
from .decorators import role_required


@role_required('master', 'admin')
def master_dashboard(request):
    if request.user.role == 'admin':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(master=request.user)
    return render(request, 'master_dashboard.html', {'orders': orders})


@role_required('master', 'admin')
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.role == 'master' and order.master != request.user:
        messages.error(request, 'Это не ваша заявка.')
        return redirect('master_dashboard')

    if request.method == 'POST':
        form = StatusChangeForm(request.POST, instance=order)
        if form.is_valid():
            old_status = order.status
            updated_order = form.save()

            if old_status != updated_order.status:
                OrderStatusHistory.objects.create(
                    order=updated_order,
                    status=updated_order.status,
                    changed_by=request.user
                )
                messages.success(request, f'Статус изменён на «{updated_order.get_status_display()}».')
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