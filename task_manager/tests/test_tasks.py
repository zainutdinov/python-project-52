import json
from pathlib import Path

from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

APP_DIR = Path(__file__).resolve().parent.parent


def from_json(file_name):
    with open(APP_DIR / 'fixtures' / file_name) as file:
        return json.load(file)


class TaskTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    test_tasks = from_json('test_tasks.json')

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.user_3 = User.objects.get(pk=3)
        self.client.force_login(self.user_1)

        self.status_1 = Status.objects.get(pk=1)
        self.status_2 = Status.objects.get(pk=2)

        self.label_1 = Label.objects.get(pk=1)
        self.label_2 = Label.objects.get(pk=2)

        self.task_1 = Task.objects.get(pk=1)
        self.task_1.label_set.set([self.label_1, self.label_2])
        self.task_2 = Task.objects.get(pk=2)
        self.tasks_count = Task.objects.count()


class TestTasksListView(TaskTestCase):
    def test_tasks_view_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('tasks_list'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks_view(self):
        response = self.client.get(reverse_lazy('tasks_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks_list.html')

    def test_tasks_columns(self):
        valid_task = self.test_tasks['list']
        response = self.client.get(reverse_lazy('tasks_list'))
        page = str(response.content)

        self.assertInHTML(f'<td>{valid_task["id"]}</td>',
                          page)
        self.assertIn(valid_task["url"], page)
        self.assertInHTML(valid_task["name"], page)
        self.assertInHTML(f'<td>{valid_task["author"]}</td>',
                          page)
        self.assertInHTML(f'<td>{valid_task["executor"]}</td>',
                          page)
        self.assertInHTML(
            f'<td>{valid_task["created_at"]}</td>',
            page
        )

    def test_tasks_rows(self):
        response = self.client.get(reverse_lazy('tasks_list'))
        page = str(response.content)

        self.assertInHTML(self.task_1.name, page)
        self.assertInHTML(self.task_2.name, page)


class TestTaskCreateView(TaskTestCase):
    def test_create_task_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('tasks_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_task_view(self):
        response = self.client.get(reverse_lazy('tasks_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks_create.html')

    def test_create_task(self):
        valid_task = self.test_tasks['create']
        response = self.client.post(reverse_lazy('tasks_create'),
                                    data=valid_task)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.tasks_count + 1)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Задача успешно создана')


class TestTaskUpdateView(TaskTestCase):
    def test_update_task_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('tasks_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_task_view(self):
        response = self.client.get(
            reverse_lazy('tasks_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks_update.html')

    def test_update_task(self):
        task_data = self.test_tasks['update']
        response = self.client.post(
            reverse_lazy('tasks_update', kwargs={'pk': 1}), data=task_data
        )
        updated_task = Task.objects.get(pk=self.task_1.pk)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.tasks_count)
        self.assertEqual(updated_task.name, task_data['name'])
        self.assertEqual(updated_task.description, task_data['description'])
        self.assertEqual(updated_task.executor.pk, task_data['executor'])
        self.assertEqual(updated_task.status.pk, task_data['status'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Задача успешно изменена')


class TestTaskDeleteView(TaskTestCase):
    def test_delete_task_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('tasks_delete', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_task_view(self):
        response = self.client.get(
            reverse_lazy('tasks_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks_delete.html')

    def test_delete_foreign_task(self):
        response = self.client.post(
            reverse_lazy('tasks_delete', kwargs={'pk': 2})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.tasks_count)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Задачу может удалить только ее автор')

    def test_delete_task(self):
        response = self.client.post(
            reverse_lazy('tasks_delete', kwargs={'pk': 1})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))

        self.assertEqual(Task.objects.count(), self.tasks_count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=self.task_1.pk)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message,
                         'Задача успешно удалена')


class TestTaskDetailView(TaskTestCase):
    def test_task_detail_if_unauthorized(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('tasks_detail', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_task_detail_view(self):
        task_data = self.test_tasks['list']
        response = self.client.get(
            reverse_lazy('tasks_detail', kwargs={'pk': 1})
        )
        page = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks_detail.html')

        self.assertInHTML(task_data['name'], page)
        self.assertInHTML(task_data['description'], page)
        self.assertInHTML(task_data['author'], page)
        self.assertInHTML(task_data['executor'], page)
        self.assertInHTML(task_data['created_at'], page)
        self.assertInHTML(task_data['label_set'][0], page)
        self.assertInHTML(task_data['label_set'][1], page)