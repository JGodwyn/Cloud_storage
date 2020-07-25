from django.urls import path, include
from . import views

urlpatterns = [
    path('user', views.UserCreateList.as_view(), name = 'user_list'),
    path('user/<int:id>', views.UserRUDList.as_view(), name = 'user_mod'),
    path('folder', views.FolderCreateList.as_view(), name = 'folder_list'),
    path('folder/<int:id>', views.FolderRUDList.as_view(), name = 'folder_mod'),
]
