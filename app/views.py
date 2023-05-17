from django.shortcuts import render
from .models import Patient
# Create your views here.

def homepage(request):
    records=Patient.objects.all().order_by('id')[:20]
    return render(request,'homepage.html',{'records':records})

def datapage(request):
    records=Patient.objects.all().order_by('id')[:500]
    return render(request,'datapage.html',{'records':records})

def classifierpage(request):
    return render(request,'classifier.html')