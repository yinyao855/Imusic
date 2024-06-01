import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin(unittest.TestCase):

    def test_login(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        el2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div/div[2]/input')))
        el2.send_keys('Nzh')
        el3 = browser.find_element(By.XPATH, '//*[@id="login"]/div/div[4]/input')
        el3.send_keys('Nzh123456')
        # 检查是否输入正确
        self.assertEqual(el2.get_attribute('value'), 'Nzh')
        self.assertEqual(el3.get_attribute('value'), 'Nzh123456')
        # 点击登录
        el4 = browser.find_element(By.XPATH, '//*[@id="login"]/div/button')
        el4.click()
        # 检查是否登录成功
        el5 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]')))
        self.assertTrue(el5)
        browser.quit()

    def test_login2(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        el2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div/div[2]/input')))
        el2.send_keys('yy')
        el3 = browser.find_element(By.XPATH, '//*[@id="login"]/div/div[4]/input')
        el3.send_keys('2003')
        # 检查是否输入正确
        self.assertEqual(el2.get_attribute('value'), 'yy')
        self.assertEqual(el3.get_attribute('value'), '2003')
        # 点击登录
        el4 = browser.find_element(By.XPATH, '//*[@id="login"]/div/button')
        el4.click()
        # 检查是否登录成功
        el5 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]')))
        self.assertTrue(el5)
        browser.quit()

if __name__ == "__main__":
    unittest.main()
