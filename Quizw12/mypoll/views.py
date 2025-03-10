from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
#endquiz
# Create your views here.
def index(request):
    hot_warm_question = get_question_hot_warm()
    hot_question = hot_warm_question["hotquestion"][:5]
    warm_question = hot_warm_question["warmquestion"][:5]
    questions = Question.objects.order_by("pk")[:5]
    return render(request, "index.html", {"questions" : questions, "hot_question" : hot_question, "warm_question" : warm_question})

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
            "questionpage.html",
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

def get_question_hot_warm():
    questions = list(Question.objects.all()) # when the numbers of question in Question is very large// will filter the latest time first.
    warm_question = []
    hot_question = []
    for question in questions:
        votes = 0
        choices = list(Choice.objects.filter(question=question))
        for choice in choices:
            votes = votes + choice.votes
        if votes >= 10 and votes < 50:
            warm_question.append((question, votes))
        elif votes >= 50:
            hot_question.append((question, votes))
    warm_question = sorted(warm_question, key=lambda x: x[1], reverse=True)
    hot_question = sorted(hot_question, key=lambda x: x[1], reverse=True)
    return {"warmquestion" : warm_question, "hotquestion" : hot_question}