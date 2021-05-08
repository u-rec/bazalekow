from django.db import models

# Create your models here.

class Category(models.IntegerChoices):
    A1 = 1, "A1"
    B = 2, "B"
    C = 3, "C"

class Indication(models.Model): # do bazy danych należy dodać od razu jako jeden element te które uznaliśmy za identyczne, żeby wyszukiwanie po bazie miało sens
    name = models.CharField(max_length=100, null=False, blank=True, default="")
    no_ind = models.BooleanField(default=False)        #wszystkie wskazania refundacyjne, pomijamy pole wskazań

    class Meta:
        ordering = ['-no_ind']

    def __str__(self):
        return self.name

class Substance(models.Model):
    name = models.CharField(max_length=75, null=False, blank=False)    # substancja czynna

    def __str__(self):
        return self.name

class Drug(models.Model):
    EAN = models.CharField(max_length=14, null=False, blank=False)     # kod EAN
    name = models.CharField(max_length=40, null=False, blank=False)    # nazwa
    form = models.CharField(max_length=30, null=True)       # postać leku 
    dose = models.IntegerField()    # dawka w miligramach (płyny: mg/g)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    content = models.CharField(max_length=60, null=True)    # zawartość opakowania
    category = models.IntegerField(choices=Category.choices)            # w którym arkuszu jest ten lek
    indications = models.ManyToManyField(Indication)
    price = models.FloatField()


    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name
