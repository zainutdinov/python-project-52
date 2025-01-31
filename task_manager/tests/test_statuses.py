from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.users.models import User

from .utils import from_json


class StatusTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json']
    test_statuses = from_json('test_statuses.json')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.status_1 = Status.objects.get(pk=1)
        self.status_2 = Status.objects.get(pk=2)
        self.status_3 = Status.objects.get(pk=3)
        self.count = Status.objects.count()


class TestStatusesListView(StatusTestCase):
    def test_status_view_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('status_list'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_status_view(self):
        response = self.client.get(reverse_lazy('status_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status_list.html')

    def test_status_columns(self):
        valid_status = self.test_statuses['list']
        response = self.client.get(reverse_lazy('status_list'))
        page = str(response.content)

        self.assertInHTML(f'<td>{valid_status["id"]}</td>',
                          page)
        self.assertInHTML(f'<td>{valid_status["name"]}</td>',
                          page)
        self.assertInHTML(
            f'<td >{valid_status["created_at"]}</td>',
            page
        )

    def test_status_rows(self):
        response = self.client.get(reverse_lazy('status_list'))
        page = str(response.content)

        self.assertInHTML(self.status_1.name, page)
        self.assertInHTML(self.status_2.name, page)
        self.assertInHTML(self.status_3.name, page)


class TestStatusCreateView(StatusTestCase):
    def test_create_status_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_status_view(self):
        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='status_create.html')

    def test_create_status(self):
        valid_status = self.test_statuses['create']
        response = self.client.post(reverse_lazy('status_create'),
                                    data=valid_status)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))
        self.assertEqual(Status.objects.count(), self.count + 1)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Статус успешно создан')


class TestStatusUpdateView(StatusTestCase):
    def test_update_status_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_status_view(self):
        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='status_update.html')

    def test_update_status(self):
        valid_status = self.test_statuses['update']
        response = self.client.post(
            reverse_lazy('status_update', kwargs={'pk': 3}),
            data=valid_status
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))
        self.assertEqual(Status.objects.get(pk=self.status_3.pk).name,
                         valid_status['name'])
        self.assertEqual(Status.objects.count(), self.count)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Статус успешно изменен')


class TestStatusDeleteView(StatusTestCase):
    def test_delete_status_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_status_view(self):
        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='status_delete.html')

    def test_delete_status_if_in_use(self):
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Невозможно удалить статус,'
                         ' потому что он используется')

    def test_delete_status(self):
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 1})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))

        self.assertEqual(Status.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.status_1.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Статус успешно удален')
