"""Purchase Amazon Products"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from amazoncaptcha import AmazonCaptcha

options = Options()
options.page_load_strategy = "eager"

login_url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fproduct%2FB09Q2NGQL8%2Fref%3Dnav_ya_signin%3Fsmid%3DA1U62USFOR8NN3%26psc%3D1&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
captcha_url = "https://www.amazon.com/errors/validateCaptcha"

class AMAZON:
    """Amazon Class"""
    def __init__(
        self,
        username: str,
        password: str
    ):
        self.username = username
        self.password = password

    def purchase(self, item_url):
        """Purchase Product"""
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        # Solve Captcha
        driver.get(captcha_url)
        img_div = driver.find_element(
            By.XPATH, "//div[@class ='a-row a-text-center']//img"
        ).get_attribute("src")
        captcha = AmazonCaptcha.fromlink(img_div)
        captcha_value = AmazonCaptcha.solve(captcha)

        driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        continue_button = driver.find_element(By.CLASS_NAME, "a-button-text")
        continue_button.click()
        try:
            # for logging into amazon
            driver.get(login_url)
            wait.until(presence_of_element_located((By.XPATH, '//*[@id="ap_email"]')))
            driver.find_element("xpath", '//*[@id="ap_email"]').send_keys(
                self.username + Keys.RETURN
            )
            driver.find_element("xpath", '//*[@id="ap_password"]').send_keys(
                self.password + Keys.RETURN
            )
        finally:
            pass

        # end of login code

        # for getting into our product page
        driver.get(item_url)

        # refresh till we find buy now button in amazon
        while not driver.find_elements("xpath", '//*[@id="buy-now-button"]'):
            driver.refresh()

        # once the button is activated ,click the buy now button
        driver.find_element("xpath", '//*[@id="buy-now-button"]').click()

        time.sleep(5)
        driver.switch_to.frame("turbo-checkout-iframe")
        time.sleep(5)
        driver.find_element("xpath", '//*[@id="turbo-checkout-pyo-button"]').click()
