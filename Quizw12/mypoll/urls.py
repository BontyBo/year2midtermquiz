from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.questionpage, name="questionpage"),
    path("<int:pk>/vote", views.vote, name="vote"),
    path("<int:pk>/result", views.result, name="result"),
]