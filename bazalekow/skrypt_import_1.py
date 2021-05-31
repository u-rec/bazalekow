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
        f = open("tekstbazy.txt", "r", encoding="cp1250")
        for line in f.readlines()[1:]:
            argumenty = line.split("$")
            if len(argumenty) >= 2:
                for substancja in argumenty[1].split("+"):
                    substancje_set.add(substancja.strip())
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
        f = open("tekstbazy.txt", "r", encoding="cp1250")
        for line in f.readlines()[1:]:
            argumenty = line.split("$")
            if len(argumenty) >= 7:
                wskazania = argumenty[6].split(";")
                if len(wskazania) == 1:
                    wskazania_set.add(re.sub("<+[0-9]>", "", wskazania[0]).strip())
                elif len(wskazania) > 1:
                    for wskazanie in wskazania:
                        wskazania_set.add(re.sub("<+[0-9]>", "", wskazanie).strip())
        for wskazania in wskazania_set:
            wskazania_obiekt = Indication(name=wskazania)
            wskazania_obiekt.save()
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)

# 1. LP 2. Substancja 3. EAN 4. Nazwa 5. Postać + Dawka 6. Zawartość 7. Wskazania 8. Odpłatność 9. Dopłata
@transaction.atomic
def importbazyleki():
    siv = transaction.savepoint()
    debug = open("debug.txt", "w")
    try:
        Drug.objects.all().delete()
        f = open("tekstbazy.txt", "r", encoding="cp1250")
        for line in f.readlines()[1:]:
            argumenty = line.split("$")
            debug.write(str(len(argumenty)) + '\n*\n')
            if len(argumenty) == 9:
                #ta substancja tutaj to mocno wstępna
                lek = Drug(name=argumenty[3], EAN=argumenty[2], substance=objects.get(argumenty[1][0].split("+").strip()),
                    form=argumenty[4], dose=argumenty[5], content=argumenty[6], category=Category.A1, price=argumenty[8])
                for wskazanie in argumenty[6].split(";"):
                    lek.indications.add(Indication.objects.get(re.sub("<+[0-9]>", "", wskazanie).strip()))
                lek.save()
        debug.close()
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)
