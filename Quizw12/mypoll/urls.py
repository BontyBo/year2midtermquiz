from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("private/", views.private_menu, name="privatepage"),
    path("<int:pk>/", views.questionpage, name="questionpage"),
    path("<int:question_pk>/vote", views.vote, name="vote"),
    path("<int:question_pk>/results", views.result, name="results"),
    # path("<str:ownercode/>", views.companypoll, name="companypoll"),
]