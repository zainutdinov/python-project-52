from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse_lazy

from .utils import from_json


class UserTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json']
    test_users = from_json('test_users.json')

    def setUp(self):
        self.client = Client()
        self.user_1 = get_user_model().objects.get(pk=1)
        self.user_2 = get_user_model().objects.get(pk=2)
        self.user_3 = get_user_model().objects.get(pk=3)
        self.users_count = get_user_model().objects.count()


class TestUsersIndexView(UserTestCase):
    def test_index_if_unauthorized(self):
        response = self.client.get(reverse_lazy('users_list'))
        user = get_user_model().objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users_list.html')
        self.assertIn(user, response.context['object_list'])

    def test_index_columns(self):
        test_user = self.test_users['list']
        response = self.client.get(reverse_lazy('users_list'))
        page = str(response.content)

        self.assertInHTML(f'<td>{test_user["id"]}</td>',
                          page)
        self.assertInHTML(f'<td>{test_user["username"]}</td>',
                          page)
        self.assertInHTML(f'<td>{test_user["full_name"]}</td>',
                          page)
        self.assertInHTML(f'<td>{test_user["date_joined"]}</td>',
                          page)

    def test_index_rows(self):
        response = self.client.get(reverse_lazy('users_list'))
        page = str(response.content)

        self.assertInHTML(self.user_1.username, page)
        self.assertInHTML(self.user_2.username, page)
        self.assertInHTML(self.user_3.username, page)


class TestUserCreateView(UserTestCase):

    def test_create_view(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse_lazy('users_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users_create.html')

    def test_create_valid_user(self):
        valid_user = self.test_users['create']['valid']
        response = self.client.post(reverse_lazy('users_create'),
                                    data=valid_user)
        objects = get_user_model().objects
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(objects.last().username, valid_user['username'])
        self.assertEqual(objects.count(), self.users_count + 1)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Пользователь успешно зарегистрирован')

    def test_create_invalid_username(self):
        invalid_user = self.test_users['create']['invalid_username']
        error_substring = ('Введите правильное имя пользователя. '
                           'Оно может содержать только буквы, '
                           'цифры и знаки @/./+/-/_.')
        response = self.client.post(reverse_lazy('users_create'),
                                    data=invalid_user)
        errors = response.context['form'].errors

        self.assertEqual(response.status_code, 200)

        self.assertIn('username', errors)
        self.assertEqual(len(errors['username']), 1)
        self.assertIn(str(error_substring), errors['username'][0])
        self.assertEqual(get_user_model().objects.count(), self.users_count)

    def test_create_invalid_password(self):
        invalid_user = self.test_users['create']['invalid_password']
        error_substring = ('Введённый пароль слишком короткий. '
                           'Он должен содержать как минимум 3 символа.')
        response = self.client.post(reverse_lazy('users_create'),
                                    data=invalid_user)
        errors = response.context['form'].errors

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(errors['password2']), 1)
        self.assertIn(str(error_substring), errors['password2'][0])
        self.assertEqual(get_user_model().objects.count(), self.users_count)

    def test_create_invalid_password_confirm(self):
        invalid_user = self.test_users['create']['invalid_password_confirm']
        error_substring = 'Введенные пароли не совпадают.'
        response = self.client.post(reverse_lazy('users_create'),
                                    data=invalid_user)
        errors = response.context['form'].errors

        self.assertEqual(response.status_code, 200)

        self.assertIn('password2', errors)
        self.assertEqual(len(errors['password2']), 1)
        self.assertIn(str(error_substring), errors['password2'][0])
        self.assertEqual(get_user_model().objects.count(), self.users_count)


class TestUserUpdateView(UserTestCase):
    def test_update_view(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse_lazy('users_update',
                                                kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users_update.html')

    def test_update_user(self):
        self.client.force_login(self.user_2)
        valid_updated_user = self.test_users['update']
        response = self.client.post(reverse_lazy('users_update',
                                                 kwargs={'pk': 2}),
                                    data=valid_updated_user)
        messages = list(get_messages(response.wsgi_request))
        user = get_user_model().objects.get(pk=2)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))

        self.assertEqual(user.username, valid_updated_user['username'])
        self.assertEqual(user.first_name, valid_updated_user['first_name'])
        self.assertEqual(user.last_name, valid_updated_user['last_name'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Пользователь успешно изменен')


class TestUserDeleteView(UserTestCase):
    def test_delete_authorized(self):
        self.client.force_login(self.user_3)
        response = self.client.get(
            reverse_lazy('users_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users_delete.html')

    def test_delete_unauthorized(self):
        response = self.client.get(
            reverse_lazy('users_delete', kwargs={'pk': 3})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_another(self):
        self.client.force_login(self.user_2)
        response = self.client.post(
            reverse_lazy('users_delete', kwargs={'pk': 1})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))

        self.assertEqual(get_user_model().objects.count(), self.users_count)
        self.assertEqual(get_user_model().objects.get(pk=1), self.user_1)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'У вас нет прав для изменения другого пользователя.')

    def test_delete_user_if_in_use(self):
        self.client.force_login(self.user_1)
        response = self.client.post(
            reverse_lazy('users_delete', kwargs={'pk': 1})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Невозможно удалить пользователя,'
                         ' потому что он используется')

    def test_delete_self(self):
        self.client.force_login(self.user_2)
        response = self.client.post(
            reverse_lazy('users_delete', kwargs={'pk': 2})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))
        self.assertEqual(get_user_model().objects.count(),
                         self.users_count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(pk=self.user_2.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Пользователь успешно удален')
