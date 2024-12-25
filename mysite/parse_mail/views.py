from django.shortcuts import render

from .mail import Mail
from .models import BaseMail


# Create your views here.
def index(request):
    return render(request, 'parse_mail/index.html')


def run_parse(request):
    a = Mail()
    a.run()


