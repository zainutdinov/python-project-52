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
                'invalid': 'Обязательное поле. Не более 150 символов. '
                           'Только буквы, цифры и символы @/./+/-/_.'
            }
        }
