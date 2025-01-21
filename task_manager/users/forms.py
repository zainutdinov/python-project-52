from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя'
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов. '
                        'Только буквы, цифры и символы @/./+/-/_.',
        }
        error_messages = {
            'username': {
                'invalid': 'Введите правильное имя пользователя. '
                           'Оно может содержать только буквы, '
                           'цифры и знаки @/./+/-/_.'
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
