from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .createExampleData import createExample

# Create your views here.

def home(request):
    if request.method == 'POST':
        ean = request.POST['ean']
        return redirect('result', ean=ean)
    return render(request, 'bazalekow/main.html')

def sresult(request, ean):
    drug = Drug.objects.get(EAN=ean)
    drugs = Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form)
    print(drugs)
    indicators = drug.indications.all()
    #indicators = Indication.objects.none()
    #for dr in drugs:
    #    indicators = indicators | dr.indications.all()
    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'tean': ean})

def example(request):
    createExample()
    return redirect('homepage')

def sresultind(request, ean, indic):
    drug = Drug.objects.get(EAN=ean)
    ind = Indication.objects.get(id=indic)
    drugs = Drug.objects.filter(substance=drug.substance).filter(indications=ind)
    indicators = drug.indications.all()
    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'tean': ean})