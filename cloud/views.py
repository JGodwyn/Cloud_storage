from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import hashers
from django.http import HttpResponseRedirect, HttpResponse
from .models import User, Folder, Files, LoggedIn
from django.db import IntegrityError
from django.urls import reverse
import os
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage


supported_format = ['jpg', 'jpeg', 'png', 'tif']


def check_login(user):  # this is not a view
    if str(user.username) in [x.username for x in LoggedIn.objects.all()]:
        return True
    else:
        return False


# the views begin over here
def welcome(request):
    return render(request, 'cloud/welcome.html')


def login(request, info = 'none'):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        for line in User.objects.all():
            if username == line.username:
                user_object = line
                if hashers.check_password(password = str(password), encoded = user_object.password):
                    # this can throw an Integrity error
                    try:
                        LoggedIn.objects.create(username = user_object.username, user_id = int(user_object.id))
                    except IntegrityError:
                        pass
                    return HttpResponseRedirect(reverse('cloud:dashboard', args = (user_object.id, )))

        return HttpResponseRedirect(reverse('cloud:login', args = ('failed', )))

    return render(request, 'cloud/login.html', {
        'info': info
    })


def sign_up(request, info):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = hashers.make_password(str(request.POST.get('password')))

        try:
            latest_user = User.objects.create(username = username, password = password)
        except IntegrityError:
            # if the name already exists
            return HttpResponseRedirect(reverse('cloud:sign_up', args = ('failed',),))

        info = 'none'
        # show the user as logged_in
        LoggedIn.objects.create(username = latest_user.username, user_id = int(latest_user.id))
        return HttpResponseRedirect(reverse('cloud:dashboard', args = (latest_user.id,)))

    return render(request, 'cloud/sign_up.html', {
        'info': info
    })


def dashboard(request, id):
    user_object = get_object_or_404(User, id = id)

    if not check_login(user_object):
        return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':

        if request.POST.get('pressed'):
            return HttpResponseRedirect(reverse('cloud:add_folder', args = (user_object.id, )))

        if request.POST.get('delete'):
            folder_id = int((request.POST.get('delete')))
            return HttpResponseRedirect(reverse('cloud:delete_folder', args = (user_object.id, folder_id, )))

        if request.POST.get('edit'):
            folder_id = int((request.POST.get('edit')))
            main_folder = Folder.objects.get(id = folder_id)
            return HttpResponseRedirect(reverse('cloud:edit_folder', args = (user_object.id, main_folder.id, )))

        return HttpResponseRedirect('#')

    return render(request, 'cloud/dashboard.html', {
        'user' : user_object
    })


def profile(request, id):
    user_object = get_object_or_404(User, id = id)

    if not check_login(user_object):
        return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        user_about = request.POST.get('about')
        user_object.about = str(user_about)
        user_object.save()

        return HttpResponseRedirect('#')

    no_files = 0
    total_size = 0
    for items in user_object.folder.all():
        no_files += items.files.count()
        for entry in items.files.all():
            total_size += entry.size

    return render(request, 'cloud/profile.html', {
        'user': user_object,
        'no_files': no_files,
        'total_size': total_size,
    })


def edit_profile(request, id, error = 'None'):
    user_object = get_object_or_404(User, id = id)

    if not check_login(user_object):
        return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        name = request.POST.get('username')
        about = request.POST.get('about')

        # get and change the logged in name
        for users in LoggedIn.objects.all():
            if users.username == user_object.username:
                logged_in_user = users

        try:
            user_object.username = name
            user_object.about = about
            user_object.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse('cloud:edit_profile', args = (user_object.id, f'{name}')))

        try:
            logged_in_user.username = name
            logged_in_user.save()
        except UnboundLocalError:
            # it shouldn't ever throw this error though
            pass

        return HttpResponseRedirect(reverse('cloud:profile', args = (user_object.id, )))

    return  render(request, 'cloud/edit_profile.html', {
        'user': user_object,
        'error': error
    })


def files(request, pk, id):
    user_object = get_object_or_404(User, id = pk)
    user_object_folder = get_object_or_404(Folder, id = id)

    if not check_login(user_object):
        return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        if request.POST.get('delete'):
            file_id = int(request.POST.get('delete'))
            user_object_file = user_object_folder.files.get(id = file_id)
            user_object_file.delete()

            return HttpResponseRedirect('#')

        try:
            if request.FILES['document']:
                document = request.FILES['document']

                # get the file extension
                file_extension = ''
                for line in str(document)[::-1]:
                    if line == '.':
                        break
                    file_extension = file_extension.__add__(line)
                file_extension = file_extension[::-1]

                # shorten the doc's name by replacing the excess digits with '...'
                short_document_name = document.name
                if len(str(document.name)) > 16:
                    short_document_name = f'{document.name[:10]}...'

                fs = FileSystemStorage()
                fs.save(document.name, document)
                base_dir = (os.path.dirname(os.path.dirname(__file__)))
                doc_dir = os.path.join(base_dir, f'media\{str(document)}')
                static_dir = os.path.join(base_dir, f'dataforms\static\media\{str(document)}')

                user_object.folder.get(id = user_object_folder.id).files.create(name = document.name, shortened_name = short_document_name, extension = file_extension, size = int(document.size)/1048576)

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect('#')

    return render(request, 'cloud/files.html', {
        'user' : user_object,
        'folder' : user_object_folder,
        'supported_format': supported_format,
    })


def add_folder(request, id):
    user_object = get_object_or_404(User, id =id)

    if not check_login(user_object):
         return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        folder_name = request.POST.get('name')
        folder_description = request.POST.get('description')
        user_object.folder.create(name = folder_name, description = folder_description)
        user_object.save()

        return HttpResponseRedirect(reverse('cloud:dashboard', args = (user_object.id, )))

    return render(request, 'cloud/add_folder.html', {
        'user' : user_object
    })


def delete_folder(request, pk, id):
    user_object = get_object_or_404(User, id =pk)
    folder_object = get_object_or_404(Folder, id = id)

    if not check_login(user_object):
         return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        if request.POST.get('option') == 'yes':
            folder_object.delete()
            user_object.save()

        return HttpResponseRedirect(reverse('cloud:dashboard', args = (user_object.id, )))

    return render(request, 'cloud/confirm_delete.html', {
        'user' : user_object,
        'folder' : folder_object
    })


def edit_folder(request, pk, id):
    user_object = get_object_or_404(User, id =pk)
    folder_object = get_object_or_404(Folder, id = id)

    if not check_login(user_object):
        return HttpResponseRedirect(reverse('cloud:login', args = ('none', )))

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        folder_object.name = name
        folder_object.description = description
        folder_object.save()

        return HttpResponseRedirect(reverse('cloud:dashboard', args = (user_object.id, )))

    return render(request, 'cloud/edit_folder.html', {
        'user' : user_object,
        'folder' : folder_object
    })


def logout(request, id):
    for line in LoggedIn.objects.all():
        if line.user_id == id:
            line.delete()

    return HttpResponseRedirect(reverse('cloud:welcome'))
