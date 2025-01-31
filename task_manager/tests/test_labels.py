from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.users.models import User

from .utils import from_json


class LabelTestCase(TestCase):
    fixtures = ['users.json', 'labels.json', 'tasks.json', 'statuses.json']
    test_labels = from_json('test_labels.json')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)
        self.client.force_login(self.user)
        self.label_1 = Label.objects.get(pk=1)
        self.label_2 = Label.objects.get(pk=2)
        self.label_3 = Label.objects.get(pk=3)
        self.count = Label.objects.count()
        self.task.labels.set([self.label_1, self.label_2])


class TestLabelsListView(LabelTestCase):
    def test_labels_view_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('labels_list'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_labels_view(self):
        response = self.client.get(reverse_lazy('labels_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels_list.html')

    def test_labels_columns(self):
        valid_label = self.test_labels['list']
        response = self.client.get(reverse_lazy('labels_list'))
        page = str(response.content)

        self.assertInHTML(f'<td>{valid_label["id"]}</td>',
                          page)
        self.assertInHTML(f'<td>{valid_label["name"]}</td>',
                          page)
        self.assertInHTML(
            f'<td>{valid_label["created_at"]}</td>',
            page
        )

    def test_labels_rows(self):
        response = self.client.get(reverse_lazy('labels_list'))
        page = str(response.content)

        self.assertInHTML(self.label_1.name, page)
        self.assertInHTML(self.label_2.name, page)
        self.assertInHTML(self.label_3.name, page)


class TestLabelCreateView(LabelTestCase):
    def test_create_label_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('labels_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_label_view(self):
        response = self.client.get(reverse_lazy('labels_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels_create.html')

    def test_create_label(self):
        valid_label = self.test_labels['create']
        response = self.client.post(reverse_lazy('labels_create'),
                                    data=valid_label)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Label.objects.count(), self.count + 1)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Метка успешно создана')


class TestLabelUpdateView(LabelTestCase):
    def test_update_label_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('labels_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_label_view(self):
        response = self.client.get(
            reverse_lazy('labels_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels_update.html')

    def test_update_label(self):
        valid_label = self.test_labels['update']
        response = self.client.post(
            reverse_lazy('labels_update', kwargs={'pk': 3}),
            data=valid_label
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Label.objects.get(pk=self.label_3.pk).name,
                         valid_label['name'])
        self.assertEqual(Label.objects.count(), self.count)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Метка успешно изменена')


class TestLabelDeleteView(LabelTestCase):
    def test_delete_label_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_label_view(self):
        response = self.client.get(
            reverse_lazy('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels_delete.html')

    def test_delete_label_if_in_use(self):
        response = self.client.post(
            reverse_lazy('labels_delete', kwargs={'pk': 1})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Невозможно удалить метку, '
                         'потому что она используется')

    def test_delete_label(self):
        response = self.client.post(
            reverse_lazy('labels_delete', kwargs={'pk': 3})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))

        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=self.label_3.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Метка успешно удалена')
