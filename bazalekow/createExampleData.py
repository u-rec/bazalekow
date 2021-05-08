from .models import *
from django.db import transaction

@transaction.atomic
def createExample():
    siv = transaction.savepoint()
    try:
        ind = Indication(name="Ból brzucha")
        ind.save()
        ind = Indication(name="Ból pleców")
        ind.save()
        ind = Indication(name="Zawał serca")
        ind.save()
        ind = Indication(no_ind=True)
        ind.save()

        subs = Substance(name="Paracetamol")
        subs.save()

        drug = Drug(name="apap", EAN="12345678901234", substance=subs, form="tabletki", dose=100,
            content="30 szt.", category=Category.A1, price=2.5)
        drug.save()
        drug.indications.add(Indication.objects.get(name="Ból brzucha"))
        drug.indications.add(Indication.objects.get(name="Ból pleców"))
        drug.save()

        drug = Drug(name="lek na zawał", EAN="01234567890123", substance=subs, form="Syropek", dose=1000,
            content="20 ml", category=Category.A1, price=100)
        drug.save()
        drug.indications.add(Indication.objects.get(name="Zawał serca"))
        drug.save()

        subs = Substance(name="sekret")
        subs.save()

        drug = Drug(name="lek na wszystko", EAN="09876543210987", substance=subs, form="Strzykawka", dose=0,
            content="5 ml", category=Category.A1, price=1000)
        drug.save()
        drug.indications.add(Indication.objects.get(no_ind=True))
        drug.save()
    except:
        transaction.savepoint_rollback(siv)
        raise Exception
    transaction.savepoint_commit(siv)


