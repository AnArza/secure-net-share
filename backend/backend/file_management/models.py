from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    owner = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    is_chunked = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)

    def __str__(self):
        return self.name

    def shared_with_user(self, user):
        return user in self.shared_with.all() or user == self.owner
