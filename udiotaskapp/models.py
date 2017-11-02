from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)

    class Meta:
        app_label = "udiotaskapp"
        verbose_name_plural = "people"

    def get_absolute_url(self):
        pass
