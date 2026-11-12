from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Comment, OrderStatusHistory


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(required=False, label='Телефон', max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            field.widget.attrs['class'] = css

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('service', 'device_type', 'description', 'photo')
        labels = {
            'service': 'Услуга (если знаете)',
            'device_type': 'Тип устройства',
            'description': 'Описание неисправности',
            'photo': 'Фото (необязательно)',
        }
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'device_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: iPhone 11, ноутбук Lenovo',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишите, что случилось с устройством',
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_device_type(self):
        device_type = self.cleaned_data['device_type'].strip()
        if len(device_type) < 3:
            raise forms.ValidationError('Укажите тип устройства (минимум 3 символа).')
        return device_type

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) < 10:
            raise forms.ValidationError('Опишите неисправность подробнее (минимум 10 символов).')
        return description      

class StatusChangeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        labels = {'status': 'Новый статус'}
        widgets = {'status': forms.Select(attrs={'class': 'form-select'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите комментарий к заявке',
            })
        }              