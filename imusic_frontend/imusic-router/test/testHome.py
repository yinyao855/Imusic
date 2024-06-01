import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestHome(unittest.TestCase):

    def test_songList(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        #点击歌单
        el6 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[3]/div/div[1]')))
        browser.execute_script("arguments[0].click();", el6)
        #检查是否进入歌单
        el7 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div')))
        browser.execute_script("arguments[0].click();", el7)
        browser.quit()

    def test_singer(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        #点击歌手
        el6 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[5]/div/div[1]')))
        browser.execute_script("arguments[0].click();", el6)
        #检查是否进入歌手
        el8 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div')))
        self.assertTrue(el8)
        browser.quit()
    def latest_song(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        #点击最新音乐
        el6 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]')))
        browser.execute_script("arguments[0].click();", el6)
        #检查是否进入最新上传
        el9 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/table')))
        self.assertTrue(el9)
        browser.quit()
    def test_search(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5173')
        wait = WebDriverWait(browser, 5)
        #点击搜索
        el5 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="query"]')))
        el5.send_keys('当')
        el6 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[6]/div/div[1]')))
        browser.execute_script("arguments[0].click();", el6)
        #检查是否进入搜索
        el10 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]')))
        self.assertTrue(el10)
        browser.quit()
if __name__ == "__main__":
    unittest.main()
