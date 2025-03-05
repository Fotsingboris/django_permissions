import logging 

logger = logging.Logger(__name__)

from django.shortcuts import render

def handler400(request, exception):
    return render(request, '400.html', status=400)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    logger.error('Internal Server Error', exc_info=True)
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)