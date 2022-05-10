from django.http import HttpResponse
from django.shortcuts import render

HTML_STRING = """ <h1> Hello World </h1>"""

#def home_view(request, *args, **kwargs):
def home_view(request):
    return render(request, 'home.html', {})