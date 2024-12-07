import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tomlkit import value


class ChromeService:
    def __init__(self):
        self.chrome_opt = webdriver.ChromeOptions()
        self.chrome_opt.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.chrome_opt)

    def wiki_count(self):
        try:
             self.driver.get(WIKI_URL)
             art_cnt = self.driver.find_element(By.XPATH, value='//*[@id="js-link-box-en"]/small')
             art_cnt = art_cnt.text
             search = self.driver.find_element(By.NAME, value='search')
             search.send_keys('Python')
             search.send_keys(Keys.ENTER)
             return art_cnt
        except Exception as err:
            logging.error(f'Unexpected error: {err}')
        finally:
            self.driver.quit()

    def brew_form(self):
        try:
            self.driver.get(BREW_URL)
            fname_bar = self.driver.find_element(By.XPATH, value='/html/body/form/input[1]')
            fname_bar.send_keys('Irfan')
            lname_bar = self.driver.find_element(By.XPATH, value='/html/body/form/input[2]')
            lname_bar.send_keys('Ahmed')
            mail_bar = self.driver.find_element(By.XPATH, value='/html/body/form/input[3]')
            mail_bar.send_keys('overlordahmed.irfan@gmail.com')
            sign_btn = self.driver.find_element(By.XPATH, value='/html/body/form/button')
            sign_btn.click()
        except Exception as err:
            logging.error(f'Unexpected error: {err}')
        finally:
            self.driver.quit()


def main():
    # keep browser open after code
    i_chrome = ChromeService()

    # art_cnt = i_chrome.wiki_count()
    # if art_cnt:
    #     logging.info(f'Retrieved Price: {art_cnt}')
    # else:
    #     logging.warning('N/A')

    i_chrome.brew_form()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    WIKI_URL = 'https://www.wikipedia.org/'
    BREW_URL = 'https://secure-retreat-92358.herokuapp.com/'

    main()