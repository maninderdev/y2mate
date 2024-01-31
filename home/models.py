from django.db import models

# Create your models here.
class Getdata(models.Model):
    # NICK NAME should be unique
    nick_name = models.CharField(max_length=20, unique =  True)

    def __str__(self):
        return self.nick_name