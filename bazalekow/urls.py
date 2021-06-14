from django.urls import path
from bazalekow import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("createExample/", views.example, name="example"),
    path("importbazy/", views.importbazy, name="importbazy"),
    path("result/<str:ean>/<int:page>", views.sresult, name="result"),
    path("result/<str:ean>/<int:page>/<int:indic>", views.sresultind, name="resultind"),
    path("random", views.rand, name="random")
]
