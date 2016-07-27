from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    abstract = models.CharField(max_length=10000)
    reads = models.IntegerField(default=0)
    stat = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.id, self.title, self.author, self.abstract, self.date_added, self.stat)


class Log(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    return_status = models.BooleanField(default=False)
    request_status = models.BooleanField(default=True)
