from django.db import models
from django.contrib.auth.models import User

class SoUser(models.Model):
    """
    This is SoUser model.
    There are user information in this model.
    But this model only for demo so only one field in this.
    """
    user = models.OneToOneField(User, verbose_name='User', related_name='souser')
    nickname = models.CharField(max_length=255)
