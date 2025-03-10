from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import LiveServerTestCase
from mypoll.models import Question, Choice

import time

class testhotwarm(LiveServerTestCase):
    fixtures=[
        'hw_choicestest.json',
        'hw_questiontest.json']
    
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def vote_hot_warm_question(self):
        self.browser.get(self.live_server_url)

        # ซีเจเข้าเว็บหน้าหลัก เห็น poll ในหัวข้อ recent question, hot question, warm question จำนวน 5, 1, 2 คำถาม
        recent_question_list = self.browser.find_element(By.ID, "recent-question")
        recent_link = recent_question_list.find_elements(By.TAG_NAME, "a")
        recent_link_text = [link.text for link in recent_link]

        hot_question_list = self.browser.find_element(By.ID, "hot-question")
        hot_link = hot_question_list.find_elements(By.TAG_NAME, "a")
        hot_link_text = [link.text for link in hot_link]

        warm_question_list = self.browser.find_element(By.ID, "warm-question")
        warm_link = warm_question_list.find_elements(By.TAG_NAME, "a")
        warm_link_text = [link.text for link in warm_link]

        current_recent_link_text = [
            "Subject", "Is it hot", "Is it warm", "Am I warm?", "Am I hot?"
        ]

        current_hot_link_text = [
            "Is it hot - 50 votes"
        ]

        current_warm_link_text = [
            "Is it warm - 22 votes",
            "Am I hot? - 49 votes"
        ]

        self.assertEqual(5, len(recent_link))
        self.assertEqual(1, len(hot_link))
        self.assertEqual(2, len(warm_link))

        for link_txt in current_recent_link_text:
            self.assertIn(link_txt, recent_link_text)

        for link_txt in current_hot_link_text:
            self.assertIn(link_txt, hot_link_text)

        for link_txt in current_warm_link_text:
            self.assertIn(link_txt, warm_link_text)

        
        # CJ สนใจคำถาม Am I warm? จึงกดเข้าไปดูเพื่อตอบคำถาม  เขาเลือกคำตอบ Yes, you are
        tobewarm = self.browser.find_element(By.LINK_TEXT, "Am I warm?")
        tobewarm.click()

        self.browser.find_element(By.ID, "choiceforYes, you are").click()
        self.browser.find_element(By.ID, "votebtn").click()

        # หน้าจอแสดงผลหน้าจำนวน vote แต่เขาไม่สนใจจึงกลับมาหน้าแรก (เขาต้องการแค่สร้างความแตกต่าง) เขาเห็นว่าตอนนี้คำถามนี้มาอยู่ใน warm question แล้ว
        self.browser.get(self.live_server_url)

        warm_question_list = self.browser.find_element(By.ID, "warm-question")
        warm_link = warm_question_list.find_elements(By.TAG_NAME, "a")
        warm_link_text = [link.text for link in warm_link]

        current_warm_link_text = [
            "Is it warm - 22 votes",
            "Am I hot? - 49 votes",
            "Am I warm? - 10 votes"
        ]

        self.assertEqual(3, len(warm_link))

        for link_txt in current_warm_link_text:
            self.assertIn(link_txt, warm_link_text)

        # เขารู้สึกสนใจในระบบ hot/warm topic มาก หัวข้อต่อไปที่เขาต้องการ vote คือ Am I hot? เขาเลือกคำตอบ Yes, you are hot now.
        tobehot = self.browser.find_element(By.LINK_TEXT, "Am I hot? - 49 votes")
        tobehot.click()

        self.browser.find_element(By.ID, "choiceforYes, you are hot now.").click()
        self.browser.find_element(By.ID, "votebtn").click()

        # เขาตื่นเต้นมากกับการเปลี่ยนแปลงเป็น hot จึงรีบกลับมาที่หน้าแรกทันที เห็นการย้ายของคำถาม Am I hot? ไปที่ Hot question
        self.browser.get(self.live_server_url)

        hot_question_list = self.browser.find_element(By.ID, "hot-question")
        hot_link = hot_question_list.find_elements(By.TAG_NAME, "a")
        hot_link_text = [link.text for link in hot_link]

        warm_question_list = self.browser.find_element(By.ID, "warm-question")
        warm_link = warm_question_list.find_elements(By.TAG_NAME, "a")
        warm_link_text = [link.text for link in warm_link]

        current_warm_link_text = [
            "Is it warm - 22 votes",
            "Am I warm? - 10 votes"
        ]

        current_hot_link_text = [
            "Is it hot - 50 votes",
            "Am I hot? - 50 votes"
        ]

        self.assertEqual(2, len(warm_link))
        self.assertEqual(2, len(hot_link))

        for link_txt in current_warm_link_text:
            self.assertIn(link_txt, warm_link_text)

        for link_txt in current_hot_link_text:
            self.assertIn(link_txt, hot_link_text)