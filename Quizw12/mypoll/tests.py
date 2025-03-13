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
        #Create Questions
        warmquestion = Question.objects.create(question_text="warm question")
        hotquestion = Question.objects.create(question_text="hot question")
        superwarmquestion = Question.objects.create(question_text="I'm warm question")
        superhotquestion = Question.objects.create(question_text="I'm very hot question")
        lonelyquestion = Question.objects.create(question_text="I'm lonely question")
        boundarywarmquestion = Question.objects.create(question_text="I have just 10 votes")
        boundaryhotquestion = Question.objects.create(question_text="I have just 50 votes")

        #Create Choices to matchs each question votes (>10 = warm question, >50 = hot question)
        Choice.objects.create(question=warmquestion, choice_text="Yes, very warm.", votes=7)
        Choice.objects.create(question=warmquestion, choice_text="No, not very warm.", votes=4)
        Choice.objects.create(question=hotquestion, choice_text="Yes, Super HOT.", votes=99)
        Choice.objects.create(question=hotquestion, choice_text="No, Not SO HOT.", votes=77)

        Choice.objects.create(question=superhotquestion, choice_text="Super HOT HOT.", votes=7322)
        Choice.objects.create(question=superwarmquestion, choice_text="So Close", votes=49)

        Choice.objects.create(question=lonelyquestion, choice_text="I'm lonely", votes=2)
        Choice.objects.create(question=boundarywarmquestion, choice_text="warm", votes=10)
        Choice.objects.create(question=boundaryhotquestion, choice_text="hot", votes=50)

    def test_get_warm_question(self):
        #get each question
        warmquestion = Question.objects.get(question_text="warm question")
        hotquestion = Question.objects.get(question_text="hot question")
        superwarmquestion = Question.objects.get(question_text="I'm warm question")
        superhotquestion = Question.objects.get(question_text="I'm very hot question")
        lonelyquestion = Question.objects.get(question_text="I'm lonely question")
        boundarywarmquestion = Question.objects.get(question_text="I have just 10 votes")
        boundaryhotquestion = Question.objects.get(question_text="I have just 50 votes")
        

        #get warm question and assert each question if it was in get question
        question = get_question_hot_warm()["warmquestion"] # return as list of pair of (question, votes)
        question = [q[0] for q in question] # get only question objects in each pair
        self.assertIn(warmquestion, question)
        self.assertIn(superwarmquestion, question)
        self.assertIn(boundarywarmquestion, question)
        self.assertNotIn(hotquestion, question)
        self.assertNotIn(superhotquestion, question)
        self.assertNotIn(boundaryhotquestion, question)
        self.assertNotIn(lonelyquestion, question)
        self.assertEqual(len(question), 3)

    def test_get_hot_question(self):
        warmquestion = Question.objects.get(question_text="warm question")
        hotquestion = Question.objects.get(question_text="hot question")
        superwarmquestion = Question.objects.get(question_text="I'm warm question")
        superhotquestion = Question.objects.get(question_text="I'm very hot question")
        lonelyquestion = Question.objects.get(question_text="I'm lonely question")
        boundarywarmquestion = Question.objects.get(question_text="I have just 10 votes")
        boundaryhotquestion = Question.objects.get(question_text="I have just 50 votes")

        #get hot question and assert each question if it was in get question
        question = get_question_hot_warm()["hotquestion"] # return as list of pair of (question, votes)
        question = [q[0] for q in question] # get only question objects in each pair
        self.assertIn(hotquestion, question)
        self.assertIn(superhotquestion, question)
        self.assertIn(boundaryhotquestion, question)
        self.assertNotIn(warmquestion, question)
        self.assertNotIn(superwarmquestion, question)
        self.assertNotIn(lonelyquestion, question)
        self.assertNotIn(boundarywarmquestion, question)
        self.assertEqual(len(question), 3)

    def test_no_private_included(self):
        # There is no private question for now
        questions = get_question_hot_warm(privatepage=True)
        self.assertFalse(questions["warmquestion"])
        self.assertFalse(questions["hotquestion"]) #test the set of private question is empty

    def test_get_right_private_hot(self):
        private_hot_question = Question.objects.create(question_text="I'm hot private.", private=True)
        private_choice = Choice.objects.create(question=private_hot_question, choice_text="Yes, private and hot.", votes=123456)
        private_warm_question = Question.objects.create(question_text="I'm warm private.", private=True)
        private_choice = Choice.objects.create(question=private_warm_question, choice_text="Yes, private and warm.", votes=19)
        questions = [q[0] for q in get_question_hot_warm(privatepage=True)["hotquestion"]]
        self.assertEqual(len(questions), 1)
        self.assertIn(private_hot_question, questions)
        self.assertNotIn(private_warm_question, questions)

    def test_get_right_private_warm(self):
        private_hot_question = Question.objects.create(question_text="I'm hot private.", private=True)
        private_choice = Choice.objects.create(question=private_hot_question, choice_text="Yes, private and hot.", votes=123456)
        private_warm_question = Question.objects.create(question_text="I'm warm private.", private=True)
        private_choice = Choice.objects.create(question=private_warm_question, choice_text="Yes, private and warm.", votes=19)
        questions = [q[0] for q in get_question_hot_warm(privatepage=True)["warmquestion"]]
        self.assertEqual(len(questions), 1)
        self.assertNotIn(private_hot_question, questions)
        self.assertIn(private_warm_question, questions)