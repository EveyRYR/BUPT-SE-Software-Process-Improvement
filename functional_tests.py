from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        # 初始化 WebDriver，这里使用 Chrome 浏览器
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # 测试结束后关闭浏览器
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项的应用
        # 他去查看了这个应用的首页
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue('1: Buy flowers' , [row.text for row in rows])

        #页面中又显示了一个文本框，可以输入其他的待办事项
        #他输入了“gift to his girlfriend”
        
        # 他访问那个URL，发现他的待办事项列表还在
        # 他满意地离开了
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
