from django.contrib import admin
from .models import User, Folder, Files, LoggedIn


class UserDisplay(admin.ModelAdmin):
    list_display = ['username', 'about', 'date_joined', 'password']


class FolderDisplay(admin.ModelAdmin):
    list_display = ['user_link', 'name', 'date_created']


class FilesDisplay(admin.ModelAdmin):
    list_display = ['name', 'extension', 'size', 'folder_link']


class LoggedInDisplay(admin.ModelAdmin):
    list_display = ['username', 'user_id', 'login_time']


admin.site.register(User, UserDisplay)
admin.site.register(Folder, FolderDisplay)
admin.site.register(Files, FilesDisplay)
admin.site.register(LoggedIn, LoggedInDisplay)
