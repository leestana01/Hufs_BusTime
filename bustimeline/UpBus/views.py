from django.shortcuts import render

def bus_list_up(request):
    return render(request, 'bus_list_up.html')
