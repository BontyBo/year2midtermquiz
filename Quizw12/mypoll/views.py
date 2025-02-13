from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
#endquiz
# Create your views here.
def index(request):
    questions = Question.objects.order_by("pk")[:5]
    return render(request, "index.html", {"questions" : questions})

def questionpage(request,pk):
    question = Question.objects.get(pk=pk)
    return render(request, 'questionpage.html', {"question" : question})

def vote(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))  

def result(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    return render(request, "results.html", {"question": question})