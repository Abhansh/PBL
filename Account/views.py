from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserFile
from .forms import SignUpForm
import os


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user)
        return Response({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

    def post(self, request):
        user = User.objects.get(username=request.user)
        data = request.data
        keys = data.keys()
        try:
            if 'first_name' in keys:
                user.first_name = data['first_name']
            if 'last_name' in keys:
                user.last_name = data['last_name']
            if 'email' in keys:
                user.email = data['email']
            user.save()
            return Response({'RESULT': 'success'})
        except Exception as e:
            return Response({'error': e})


class SignupView(APIView):
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            os.mkdir('Files/{}'.format(form.data['username']))
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            response = {'RESULT': 'success'}
        else:
            error = dict(form.errors)
            print(error)
            response = error

        return Response(response)


class GetFileListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        username = request.user
        user = User.objects.get(username=username)
        files = UserFile.objects.values('file_name').filter(user=user)
        return Response(files)


class FileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, filename):
        path = 'Files/{}/{}'.format(request.user, filename)
        with open(path) as file:
            code = file.read()
            return Response(code)

    def put(self, request, filename):
        username = request.user
        user = User.objects.get(username=username)
        path = 'Files/{}/'.format(user.username)
        file_type = filename[filename.find('.'):]
        file = open(path + filename, 'w')
        file.close()
        file_instance = UserFile.objects.create(user=user, file_name=filename, file_type=file_type)
        file_instance.save()
        return Response({'success': 'success'})

    def delete(self, request, filename):
        username = request.user
        user = User.objects.get(username=username)
        path = 'Files/{}/'.format(user.username)
        file_instance = UserFile.objects.get(user=user, file_name=filename)
        file_instance.delete()
        os.remove(path=path + filename)
        return Response({'success': 'success'})
