from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .createExampleData import createExample
from .skrypt_import_1 import *

# Create your views here.

wszystko = "We wszystkich zarejestrowanych wskazaniach na dzień wydania decyzji"

def home(request):
    if request.method == 'POST':
        ean = request.POST['ean']
        return redirect('result', ean=ean, page=0)
    return render(request, 'bazalekow/main.html')

def sresult(request, ean, page):
    if page < 0:
        return redirect('result', ean=ean, page=0)
    drug = Drug.objects.filter(EAN=ean)
    if len(drug) != 1:
        return render(request, 'bazalekow/notfound.html')
    drug = drug[0]
    drugs = Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form)
    print(drugs)
    indicators = drug.indications.all().exclude(name=wszystko)
    if indicators[0].no_ind == True:
        indicators = indicators[:1]
    # elif indicators[0].name == wszystko:
    #     indicators = indicators[1:]
    #indicators = Indication.objects.none()
    #for dr in drugs:
    #    indicators = indicators | dr.indications.all()
    if len(drugs) > page * 30:
        drugs = drugs[(page * 30):]
    else:
        return redirect('result', ean=ean, page=((len(drugs) - 1) // 30))
    if len(drugs) > 30:
        drugs = drugs[:30]
    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'tean': ean, 'page': page})

def example(request):
    createExample()
    return redirect('homepage')

def importbazy(request):
    importbazysubstancje()
    importbazywskazania()
    importbazyleki()
    return redirect('homepage')

def sresultind(request, ean, page, indic):
    if page < 0:
        return redirect('result', ean=ean, page=0)
    drug = Drug.objects.filter(EAN=ean)
    indicat = Indication.objects.filter(id=indic)
    if len(drug) != 1 or len(indicat) != 1:
        return render(request, 'bazalekow/notfound.html')
    drug = drug[0]
    indicat = indicat[0]
    if indicat.name == wszystko or indicat.no_ind == True:
        return redirect('result', ean=ean, page=page)
    drugs = Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(indications=indicat)
    print(drugs)
    indicators = drug.indications.all().exclude(name=wszystko)
    if indicators[0].no_ind == True:
        indicators = indicators[:1]
    # elif indicators[0].name == wszystko:
    #     indicators = indicators[1:]
    #indicators = Indication.objects.none()
    #for dr in drugs:
    #    indicators = indicators | dr.indications.all()
    if len(drugs) > page * 30:
        drugs = drugs[(page * 30):]
    else:
        return redirect('result', ean=ean, page=((len(drugs) - 1) // 30))
    if len(drugs) > 30:
        drugs = drugs[:30]
    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'tean': ean, 'page': page})

