from django.db import models
from django.contrib.auth import get_user_model


class UserFile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=10)

    def __str__(self):
        return str(self.file_name) + ' ' + str(self.user)
