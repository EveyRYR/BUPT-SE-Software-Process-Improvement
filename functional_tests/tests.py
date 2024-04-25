from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from lists.models import Item
from django.test import TestCase

MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        # 初始化 WebDriver，这里使用 Chrome 浏览器
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # 测试结束后关闭浏览器
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项的应用
        # 他去查看了这个应用的首页
        self.browser.get(self.live_server_url)

        # 他注意到网页的标题和头部都包含了“To-Do”这个词
        self.assertIn('To-Do', self.browser.title, "Browser title was: " + self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用提供了一个输入待办事项的文本框
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 他在文本输入框中输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')

        # 他按了回车键后，页面更新了
        # 待办事项列表中显示了“1: Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy flowers')
        
        #页面中又显示了一个文本框，可以输入其他的待办事项
        #他输入了“gift to his girlfriend”
        inputbox= self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        # 他访问那个URL，发现他的待办事项列表还在
        # 他满意地离开了
        # self.fail('Finish the test!')

    def test_multuple_users_can_start_lists_at_different_urls(self):
        #张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')
        #他注意到清单有个唯一的 URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')
        #现在一个新用户王五访问了网站
        #我们使用一个新浏览器会话
        #确保张三的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Chrome()

        #王五访问首页
        #页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('Give a gift to Lisi',page_text)

        #王五输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        #王五获得了他的唯一URL
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)
        #这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)
        #两人都很满意，然后去睡觉了
