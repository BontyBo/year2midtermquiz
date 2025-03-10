from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from .models import Question, Choice
from mypoll.views import questionpage,vote, get_question_hot_warm

# Create your tests here.
class testPollPage(TestCase):
    fixtures=[
        'mypoll/fixtures/mypollquestions.json',
        'mypoll/fixtures/mypollchoices.json']
    
    def test_poll_contain_all_choices(self):
        request = HttpRequest()
        question = Question.objects.get(question_text="Subject")
        response = questionpage(request,question.pk)
        html = response.content.decode("utf8")
        for choice in question.choice_set.all():
            self.assertIn(choice.choice_text, html)
        print("Poll contains all data")

    def test_vote_add_votes(self):
        question = Question.objects.get(question_text="Subject")
        choice = question.choice_set.get(choice_text="math")
        before = choice.votes

        post_data = {
            "choice" : choice.pk
        }
        urls = reverse('polls:vote', args=[question.pk])

        self.client.post(urls, post_data)
        
        choice.refresh_from_db()
        after = choice.votes
        self.assertEqual(after, before+1)
        print("vote add a vote to database")

    def test_vote_nothing(self):
        question = Question.objects.get(question_text="Subject")
        post_data = {}

        url = reverse('polls:vote', args=[question.pk])
        response = self.client.post(url, post_data)
        context = response.context
        self.assertEqual(context['error_message'], "You didn't select a choice.")
        print("vote nothing show right error message")

class test_get_question(TestCase):
    def setUp(self):
        warmquestion = Question.objects.create(question_text="warm question")
        hotquestion = Question.objects.create(question_text="hot question")

        Choice.objects.create(question=warmquestion, choice_text="Yes, very warm.", votes=7)
        Choice.objects.create(question=warmquestion, choice_text="No, not very warm.", votes=9)
        Choice.objects.create(question=hotquestion, choice_text="Yes, Super HOT.", votes=99)
        Choice.objects.create(question=hotquestion, choice_text="No, Not SO HOT.", votes=77)

    def test_get_warm_question(self):
        warmquestion = Question.objects.get(question_text="warm question")
        hotquestion = Question.objects.get(question_text="hot question")
        question = get_question_hot_warm()["warmquestion"]
        self.assertIn(warmquestion, question)
        self.assertNotIn(hotquestion, question)

    def test_get_hot_question(self):
        warmquestion = Question.objects.get(question_text="warm question")
        hotquestion = Question.objects.get(question_text="hot question")
        question = get_question_hot_warm()["hotquestion"]
        self.assertIn(hotquestion, question)
        self.assertNotIn(warmquestion, question)