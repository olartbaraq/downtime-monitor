from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.


class Historicallogs(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    websites = models.TextField() #url of the website
    is_url_valid = models.CharField(default=None, max_length=100)
    timestamp = models.DateTimeField(default=None)
    # notification = models.CharField(max_length=30, default=None, null=False)
    is_active = models.CharField(default=None, max_length=100)


    def __str__(self):
        return self.websites
