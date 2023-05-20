from django.shortcuts import render

def bus_list_up(request):
    return render(request, 'bus_list_up.html')

def mainPage(request):
    return render(request, 'mainPage.html')