from django.contrib import admin
from .models import Indication, Drug, Substance
# Register your models here.

admin.site.register(Indication)
admin.site.register(Drug)
admin.site.register(Substance)