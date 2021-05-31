from bazalekow.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import re

#http://127.0.0.1:8000/importbazy/
@transaction.atomic
def importbazysubstancje():
    siv = transaction.savepoint()
    try:
        Substance.objects.all().delete()
        substancje_set = set()
        f = open("baza_tsv_A1.tsv", "r", encoding="utf-8")
        for line in f.readlines()[1:]:
            argumenty = line.split("\t")
            if len(argumenty) == 10:
                sub = argumenty[1].strip().casefold()
                substancje_set.add(sub)
        for substancja in substancje_set:
            substancja_obiekt = Substance(name=substancja)
            substancja_obiekt.save()
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)

@transaction.atomic
def importbazywskazania():
    siv = transaction.savepoint()
    try:
        Indication.objects.all().delete()
        wskazania_set = set()
        f = open("baza_tsv_A1.tsv", "r", encoding="utf-8")
        for line in f.readlines()[1:]:
            argumenty = line.split("\t")
            if len(argumenty) == 10:
                wskazania = argumenty[7].replace('\"','').split(";")
                for wskazanie in wskazania:
                    wskazania_set.add(re.sub("<+[0-9]>", "", wskazanie).strip().casefold())
        for wskazania in wskazania_set:
            wskazania_obiekt = Indication(name=wskazania)
            wskazania_obiekt.save()
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)

#LP	Substancja	EAN	Nazwa	Postać	Dawka	Zawartość	Wskazania	Odpłatność	Dopłata
@transaction.atomic
def importbazyleki():
    siv = transaction.savepoint()
    try:
        Drug.objects.all().delete()
        f = open("baza_tsv_A1.tsv", "r", encoding="utf-8")
        for line in f.readlines()[1:]:
            argumenty = line.split("\t")
            if len(argumenty) == 10:
                substancja = argumenty[1].strip().casefold()
                lek = Drug(name=argumenty[3], EAN=argumenty[2], substance=Substance.objects.get(name=substancja), form=argumenty[4], dose=argumenty[5], content=argumenty[6], category=Category.A1, price=argumenty[9].replace(",", "."))
                lek.save()
                for wskazanie in argumenty[7].replace('\"','').split(";"):
                    jakie = re.sub("<+[0-9]>", "", wskazanie).strip().casefold()
                    lek.indications.add(Indication.objects.get(name=jakie))
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)
