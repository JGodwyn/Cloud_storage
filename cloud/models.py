from django.db import models


class User(models.Model):
    username = models.CharField(max_length = 200, unique = True, null = False)
    password = models.CharField(max_length = 20000, null = False)
    about = models.TextField(max_length = 20000, null = True)
    date_joined = models.DateTimeField(auto_now_add = True)

    @property  # this is used in permissions for the API view
    def owner(self):
        return self.username

    def __str__(self):
        return self.username


class Folder(models.Model):
    user_link = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'folder')
    name = models.CharField(max_length = 2000, unique = False, null = False)
    description = models.TextField(max_length = 1000, null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name


class Files(models.Model):
    folder_link = models.ForeignKey(Folder, on_delete = models.CASCADE, related_name = 'files')
    name = models.CharField(max_length = 500)
    shortened_name = models.CharField(max_length = 250)
    extension = models.CharField(max_length = 50)
    size = models.DecimalField(max_digits = 900, decimal_places = 2)

    class Meta:
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.name}  >>>  {self.extension, self.size}'


class LoggedIn(models.Model):
    login_time = models.DateTimeField(auto_now = True)
    username = models.CharField(max_length = 200, unique = True, null = False)
    user_id = models.IntegerField(null = False)

    def __str__(self):
        return f' logged in: {self.username} on {self.login_time}'
