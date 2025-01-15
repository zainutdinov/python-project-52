from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'