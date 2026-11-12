from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
        # Добавляем Bootstrap-классы ко всем полям
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