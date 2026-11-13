from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('master', 'Мастер'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    quantity_in_stock = models.PositiveIntegerField(default=0, verbose_name='Остаток на складе')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} (остаток: {self.quantity_in_stock})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Принята'),
        ('diagnostics', 'В диагностике'),
        ('repair', 'В ремонте'),
        ('ready', 'Готова к выдаче'),
        ('issued', 'Выдана'),
    ]

    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='client_orders',
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='master_orders',
        verbose_name='Мастер'
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Услуга'
    )
    device_type = models.CharField(
    max_length=200, 
    validators=[MinLengthValidator(3)], 
    verbose_name='Тип устройства'
    )
    description = models.TextField(verbose_name='Описание неисправности')
    photo = models.ImageField(upload_to='orders/', blank=True, null=True, verbose_name='Фото')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='accepted', verbose_name='Статус'
    )
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Стоимость работ'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"Заявка #{self.id} — {self.device_type} ({self.get_status_display()})"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'История статуса'
        verbose_name_plural = 'История статусов'

    def __str__(self):
        return f"Заявка #{self.order.id}: {self.get_status_display()}"


class OrderPart(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='used_parts'
    )
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    quantity_used = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.part.name} × {self.quantity_used} (заявка #{self.order.id})"


class Comment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.author.username} к заявке #{self.order.id}"