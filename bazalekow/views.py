from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .createExampleData import createExample
from .skrypt_import_1 import *

# Create your views here.

wszystko = "we wszystkich zarejestrowanych wskazaniach na dzień wydania decyzji"

def home(request):
    if request.method == 'POST':
        ean = request.POST['ean']
        return redirect('result', ean=ean, page=0)
    return render(request, 'bazalekow/main.html')

def sresult(request, ean, page):
    if page < 0:
        return redirect('result', ean=ean, page=0)
    drug = Drug.objects.filter(EAN=ean)
    if len(drug) < 1:
        return render(request, 'bazalekow/notfound.html')
    indicators = Indication.objects.none()
    for dr in drug:
        indicators = indicators | dr.indications.all().exclude(name=wszystko)
    drug = drug[0]
    drugs = Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form)
    pfustatus = 0
    if len(Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(priceForUnit=-1)) > 0:
        pfustatus = -1
    if len(Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(priceForUnit=-2)) > 0:
        pfustatus = -2
    # print(drugs)
    if len(indicators) == 0:
        indicators = [Indication(name="", no_ind=True)]
    # if indicators[0].no_ind == True:
    #     indicators = indicators[:1]
    # elif indicators[0].name == wszystko:
    #     indicators = indicators[1:]
    #indicators = Indication.objects.none()
    #for dr in drugs:
    #    indicators = indicators | dr.indications.all()

    nextbutton = 0
    prevbutton = 0

    if len(drugs) > (page+1)*30:
        nextbutton = '/result/' + ean + '/' + str(page+1)

    if page-1 >= 0:
        prevbutton = '/result/' + ean + '/' + str(page-1)

    if len(drugs) > page * 30:
        drugs = drugs[(page * 30):]
    else:
        return redirect('result', ean=ean, page=((len(drugs) - 1) // 30))
    
    if len(drugs) > 30:
        drugs = drugs[:30]

    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'prevbutton': prevbutton, 'nextbutton': nextbutton, 'tean': ean, 'page': page, 'pfustatus': pfustatus})

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
    if len(drug) < 1 or len(indicat) != 1:
        return render(request, 'bazalekow/notfound.html')
    indicators = Indication.objects.none()
    for dr in drug:
        indicators = indicators | dr.indications.all().exclude(name=wszystko)
    drug = drug[0]
    indicat = indicat[0]
    if indicat.name == wszystko or indicat.no_ind == True:
        return redirect('result', ean=ean, page=page)
    drugs = Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(indications=indicat)
    pfustatus = 0
    if len(Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(indications=indicat).filter(priceForUnit=-1)) > 0:
        pfustatus = -1
    if len(Drug.objects.filter(substance=drug.substance).filter(dose=drug.dose).filter(form=drug.form).filter(indications=indicat).filter(priceForUnit=-2)) > 0:
        pfustatus = -2
    
    nextbutton = 0
    prevbutton = 0

    if len(drugs) > (page+1)*30:
        nextbutton = '/result/' + ean + '/' + str(page+1) + '/' + str(indic)

    if page-1 >= 0:
        prevbutton = '/result/' + ean + '/' + str(page-1) + '/' + str(indic)

    # indicators = drug.indications.all().exclude(name=wszystko)
    if len(indicators) == 0:
        indicators = [Indication(name="", no_ind=True)]
    # if indicators[0].no_ind == True:
    #     indicators = indicators[:1]
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
    return render(request, 'bazalekow/results.html', {'drugs': drugs, 'indicators': indicators, 'prevbutton': prevbutton, 'nextbutton': nextbutton, 'tean': ean, 'page': page, 'pfustatus': pfustatus})

def rand(request):
    import random
    random_idx = random.randint(0, Drug.objects.count() - 1)
    randomEan = Drug.objects.all()[random_idx].EAN
    return redirect("result", ean=randomEan, page=0)