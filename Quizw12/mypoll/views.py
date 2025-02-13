from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice

# Create your views here.
def index(request):
    questions = Question.objects.order_by("pk")[:5]
    return render(request, "index.html", {"questions" : questions})

def questionpage(request,pk):
    question = Question.objects.get(pk=pk)
    return render(request, 'questionpage.html', {"question" : question})

def vote(request):
    pass

def result(request):
    pass