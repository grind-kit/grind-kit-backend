from django.shortcuts import render
from django.http import JsonResponse

def getRoutes (request):
    routes = [
        {
            'Endpoint': '/instancecontent',
            'method': 'GET',
            'body': 'Hello World',
            'description': 'Returns an array of instance content'
        },
    ]

    return JsonResponse(routes, safe=False)