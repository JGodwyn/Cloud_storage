from django.urls import path, include
from . import views


app_name = 'cloud'
urlpatterns = [
    path('', views.welcome, name = 'welcome'),
    path('home/<str:info>', views.login, name = 'login'),
    path('signup/<str:info>', views.sign_up, name = 'sign_up'),
    path('dashboard/val<int:id>field', views.dashboard, name = 'dashboard'),
    path('dashboard/val<int:pk>field/foldthis<int:id>file', views.files, name = 'files'),
    path('dashboard/val<int:id>field/Newfolder', views.add_folder, name = 'add_folder'),
    path('dashboard/val<int:pk>field/Delfolder<int:id>', views.delete_folder, name = 'delete_folder'),
    path('dashboard/val<int:pk>field/Edifolder<int:id>', views.edit_folder, name = 'edit_folder'),
    path('dashboard/logout/<int:id>', views.logout, name = 'log_out'),
    path('dashboard/<int:id>/profile', views.profile, name = 'profile'),
    path('dashboard/<int:id>/edit/<str:error>', views.edit_profile, name = 'edit_profile'),
    path('about', views.about, name = 'about')

]
