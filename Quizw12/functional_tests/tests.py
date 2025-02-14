from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import LiveServerTestCase
from mypoll.models import Question, Choice

import time

class testPoll(LiveServerTestCase):
    fixtures=[
        'mypoll/fixtures/mypollquestions.json',
        'mypoll/fixtures/mypollchoices.json']
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        #question = Question.objects.create(question_text="Subject")
        #Choice.objects.create(question=question, choice_text="math", votes=0)
        #Choice.objects.create(question=question, choice_text="science", votes=0)
        #Choice.objects.create(question=question, choice_text="english", votes=0) 

    def tearDown(self):
        self.browser.quit()

    def test_vote_my_poll(self):
        #A เห็นลิงค์แสดงคำว่า Subject แล้วกดเข้าไป
        self.browser.get(self.live_server_url)
        time.sleep(2)
        subject_poll = self.browser.find_element(By.LINK_TEXT, "Subject")
        subject_poll.click()

        #A มีตัวเลือกแสดงคำว่า math, science, english
        math_choice = self.browser.find_element(By.ID, "choice-math")
        self.assertIn(math_choice.text, "math")
        math_choice = self.browser.find_element(By.ID, "choice-science")
        self.assertIn(math_choice.text, "science")
        math_choice = self.browser.find_element(By.ID, "choice-english")
        self.assertIn(math_choice.text, "english")

        #A กดตัวเลือกที่เขียนว่า math
        math_radio = self.browser.find_element(By.ID, "choiceformath")
        math_radio.click()

        #A กดปุ่มที่เขียนว่า vote
        vote_btn = self.browser.find_element(By.ID, "votebtn")
        vote_btn.click()

        #A เห็นหน้าจอแสดง math -- 1vote, science -- 0 votes, english -- 0 votes
        math_choice = self.browser.find_element(By.ID, "math-score")
        self.assertIn(math_choice.text, "math -- 1 vote")
        math_choice = self.browser.find_element(By.ID, "science-score")
        self.assertIn(math_choice.text, "science -- 0 votes")
        math_choice = self.browser.find_element(By.ID, "english-score")
        self.assertIn(math_choice.text, "english -- 0 votes")

        #A เห็นลิงค์ Vote again? แล้วกด
        vote_agn = self.browser.find_element(By.LINK_TEXT, "Vote again?")
        vote_agn.click()