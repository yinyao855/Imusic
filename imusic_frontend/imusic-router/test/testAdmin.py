import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAdmin(unittest.TestCase):

    def test_admin_song(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        el1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]')))
        browser.execute_script("arguments[0].scrollIntoView();", el1)
        action = ActionChains(browser)
        action.move_to_element(el1).click().perform()
        el2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div/div[2]/input')))
        el2.send_keys('Nzh')
        el3 = browser.find_element(By.XPATH, '//*[@id="login"]/div/div[4]/input')
        el3.send_keys('Nzh123456')
        # 检查是否输入正确
        time.sleep(1)
        # 点击登录
        el4 = browser.find_element(By.XPATH, '//*[@id="login"]/div/button')
        browser.execute_script("arguments[0].scrollIntoView();", el4)
        action = ActionChains(browser)
        action.move_to_element(el4).click().perform()
        time.sleep(5)
        el5 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]')))
        browser.execute_script("arguments[0].scrollIntoView();", el5)
        action = ActionChains(browser)
        action.move_to_element(el5).click().perform()
        time.sleep(1)
        # 检查是否进入歌曲管理
        el7 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]')))
        browser.execute_script("arguments[0].scrollIntoView();", el7)
        action = ActionChains(browser)
        action.move_to_element(el7).click().perform()

        el8 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,r'#app > div.flex.w-full.h-screen.bg-zinc-900 > div.w-full.lg\:w-5\/6.h-full.mr-0 > div > div.w-full.h-16.pl-6.fixed.bg-zinc-900.z-50 > div.text-base.inline-block.mx-5.w-30.rounded-lg.antialiased.tracking-widest.font-medium.transition-colors.duration-400.hover\:bg-gray-600\/40.cursor-pointer.text-cyan-700.underline.underline-offset-8.decoration-2.text-transition')))
        browser.execute_script("arguments[0].scrollIntoView();", el8)
        action = ActionChains(browser)
        action.move_to_element(el8).click().perform()
        time.sleep(5)
        el9 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, r'#app > div.flex.w-full.h-screen.bg-zinc-900 > div.w-full.lg\:w-5\/6.h-full.mr-0 > div > div.w-full.mt-16 > div.overflow-x-auto.mx-4 > table')))
        self.assertTrue(el9)
        browser.quit()

    def test_admin_songList(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        el1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]')))
        browser.execute_script("arguments[0].scrollIntoView();", el1)
        action = ActionChains(browser)
        action.move_to_element(el1).click().perform()
        el2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div/div[2]/input')))
        el2.send_keys('Nzh')
        el3 = browser.find_element(By.XPATH, '//*[@id="login"]/div/div[4]/input')
        el3.send_keys('Nzh123456')
        # 检查是否输入正确
        self.assertEqual(el2.get_attribute('value'), 'Nzh')
        self.assertEqual(el3.get_attribute('value'), 'Nzh123456')
        # 点击登录
        el4 = browser.find_element(By.XPATH, '//*[@id="login"]/div/button')
        browser.execute_script("arguments[0].scrollIntoView();", el4)
        action = ActionChains(browser)
        action.move_to_element(el4).click().perform()
        # 检查是否登录成功
        time.sleep(5)
        el6 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]')))
        browser.execute_script("arguments[0].scrollIntoView();", el6)
        action = ActionChains(browser)
        action.move_to_element(el6).click().perform()
        # 检查是否进入歌单管理
        el7 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]')))
        self.assertTrue(el7)
        browser.quit()

if __name__ == "__main__":
    unittest.main()
