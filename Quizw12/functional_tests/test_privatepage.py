from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import LiveServerTestCase

import time

class Test_Private_page(LiveServerTestCase):
    fixtures=[
        'fixtures/Q_for_private_test.json',
        'fixtures/A_for_private_test.json']
    
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_go_to_private_page(self):
        # Jim คุ้นเคยกับเว็บเราอย่างดีและเขาก็มาเข้ามาในเว็บ เขาเห็นลิงค์ 5 อันแสดงคำถามล่าสุด
        
        self.browser.get(self.live_server_url)
        recent_question_list = self.browser.find_element(By.ID, "recent-question")
        recent_link = recent_question_list.find_elements(By.TAG_NAME, "a")
        
        recent_link_text = [link.text for link in recent_link]

        current_recent_link_text = [
            "Subject", "Is it hot", "Is it warm", "Am I warm?", "Am I hot?"
        ]

        self.assertEqual(5, len(recent_link))
        for link_txt in current_recent_link_text:
            self.assertIn(link_txt, recent_link_text)
        time.sleep(2)

        # แต่ว่าเขาเป็นบุคคลพิเศษทำให้เขารู้ว่ามีหน้าลับซ่อนอยู่ ซึ่งก็คือหน้า private เขาเห็นคำถามลับของเรา 3 คำถาม

        self.browser.get(self.live_server_url+"/private")
        private_question_list = self.browser.find_element(By.ID, "private-question")
        private_link = private_question_list.find_elements(By.TAG_NAME, "a")
        
        private_link_text = [link.text for link in private_link]

        current_private_link_text = [
            "What is your favorite color?", "Am I private?", "What is your dog's name?"
        ]

        self.assertEqual(3, len(private_link))
        for link_txt in current_private_link_text:
            self.assertIn(link_txt, private_link_text)
        time.sleep(2)

        # เขาอยากบอกสีที่ชอบให้โลกรู้ เขาเลือกหัวข้อสี แล้วเลือกสีแดงและกด vote
        self.browser.find_element(By.LINK_TEXT, "What is your favorite color?").click()
        time.sleep(1)
        self.browser.find_element(By.ID, "choiceforred").click()
        self.browser.find_element(By.ID, "votebtn").click()
        time.sleep(1)

        # เขาก็มาที่หน้าแสดงผลลัพธ์ เขาพอใจแล้วกดออก
        self.assertIn("results", self.browser.current_url)