from django.db import models


# Create your models here.
class BaseMail(models.Model):
    email = models.CharField(max_length=64, verbose_name='email', unique=True)
    name = models.CharField(max_length=128, verbose_name='Имена в почте')
    email_in_body = models.CharField(max_length=255, verbose_name='Почтовые имена в теле письма')
    phones = models.CharField(max_length=255, verbose_name='Телефоны в письме')

    def __str__(self):
        return self.email
