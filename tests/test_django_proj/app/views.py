# -*- coding: utf-8 -*-
from django.http import HttpResponse
from autoroute import route

@route()
def auto_generated(request):
    return HttpResponse("A default auto-generated route")

@route(name='with-name')
def with_name(request):
    return HttpResponse("A route with name.")

@route(url='/custom/',name='custom-name')
def custom_route(request):
    return HttpResponse("This is a custom route.")
