from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import LiveServerTestCase
from mypoll.models import Question, Choice

import time

class Test_Com_Poll(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_vote_hot_warm_question(self):
        # ร้านค้าให้ url กับ Joe เพื่อแสดงความพึงพอใจกับสินค้าที่ซื้อไป

        # Joe เข้ามาที่ลิงก์ Poll ที่ร้านค้าให้

        # Joe เห็นคำถามเกี่ยวกับ ขวดน้ำ และ cookie

        # Joe เลือก Cookie เพราะเขาพิ่งซื้อ Cookie มา

        # เขาให้คะแนนความพึงพอใจระดับ 5 เพราะเขาชอบมันมาก

        # เขาเห็นว่ามีจำนวนคน vote ให้ 5 อีก 20 คนด้วยกัน และ ที่เหลือให้ 3 อีก 3 คน
        # เขาพอใจที่คนส่วนมากเห็นด้วยกับเขา เขาจึงกดปิด
        pass