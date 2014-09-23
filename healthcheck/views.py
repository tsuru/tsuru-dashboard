from django.http import HttpResponse


def healthcheck(request):
    return HttpResponse("WORKING", status=200)
