from django.contrib.auth.models import User


def __str__(self):
    return self.get_full_name()


User.add_to_class('__str__', __str__)
User.add_to_class('full_name', __str__)
