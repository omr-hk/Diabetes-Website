from django.shortcuts import render,redirect
from .models import Patient,Poll
from .classifier import *
# Create your views here.



def homepage(request):
    records=Patient.objects.all().order_by('id')[:20]
    return render(request,'homepage.html',{'records':records})

def datapage(request):
    records=Patient.objects.all().order_by('id')[:500]
    return render(request,'datapage.html',{'records':records})

def classifierpage(request):
    return render(request,'classifier.html')

def predictpage(request):
    gender=request.GET['gender']
    age=request.GET['age']
    hyper=request.GET['hypertension']
    heart=request.GET['heart_disease']
    smk=request.GET['smoking_history']
    bmi=float(request.GET['bmi'])
    hba=float(request.GET['HbA1c_level'])
    bcl=request.GET['blood_glucose_level']
    params={'gen':gender,'ag':int(age),
            'hyp':int(hyper),
            'heart':int(heart),
            'smk':smk,
            'bmi':round(bmi,2),
            'hba':round(hba,1),
            'bcl':int(bcl)}
    result=classify(params=params).predictResult()
    params['result']=result
    try:
        score=Poll.objects.get(id=0)
    except:
        Poll.objects.create(id=0,correct=0,incorrect=0)
    score=Poll.objects.get(id=0)
    params['score']=score
    return render(request,'predictpage.html',params)

def pollpage(request):
    score=Poll.objects.get(id=0)
    if 'correct' in request.POST:
        score.correct+=1
        score.save()
    elif 'incorrect' in request.POST:
        score.incorrect+=1
        score.save()
    else:
        score.save()
    return classifierpage(request)
    