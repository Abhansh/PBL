from django.shortcuts import render


def code(request):
    return render(request, 'Code/code.html')
