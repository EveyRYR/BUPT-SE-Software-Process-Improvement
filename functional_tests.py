from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        # 应用提供了一个输入待办事项的文本框
        # 他在文本输入框中输入了“Buy flowers”
        # 张三做了一些事情...

        # 他访问那个URL，发现他的待办事项列表还在
        # 他满意地离开了

if __name__ == '__main__':
    unittest.main()
