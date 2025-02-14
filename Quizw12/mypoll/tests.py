from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from .models import Question, Choice
from mypoll.views import questionpage,vote

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