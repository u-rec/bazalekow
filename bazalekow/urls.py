from django.urls import path
from bazalekow import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("result/<str:ean>", views.sresult, name="result"),
    path("createExample/", views.example, name="example"),
    path("result/<str:ean>/<int:indic>", views.sresultind, name="resultind")
]