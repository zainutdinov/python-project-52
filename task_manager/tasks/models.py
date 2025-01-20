from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='authored_tasks')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                                 blank=True, related_name='executed_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    label_set = models.ManyToManyField(Label, through='Membership', blank=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Membership(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
