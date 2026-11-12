from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .decorators import role_required


@role_required('client')
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.status = 'accepted'
            order.save()
            messages.success(request, f'Заявка #{order.id} создана! Мы свяжемся с вами.')
            return redirect('catalog')
    else:
        form = OrderForm()

    return render(request, 'order_create.html', {'form': form})