import logging
from selenium import webdriver
from selenium.webdriver.common.by import By


class ChromeService:
    def __init__(self):
        self.chrome_opt = webdriver.ChromeOptions()
        self.chrome_opt.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.chrome_opt)

    def amazon_price(self):
        try:
            self.driver.get(AMAZON_URL)
            price_dollar = self.driver.find_element(By.CLASS_NAME, value='a-price-whole').text
            price_cents = self.driver.find_element(By.CLASS_NAME, value='a-price-fraction').text

            return f'{price_dollar}.{price_cents}'

        except Exception as err:
            logging.error(f'Unexpected error: {err}')
        finally:
            self.driver.quit()

    def wiki_count(self):
        try:
             self.driver.get(WIKI_URL)
             art_cnt = self.driver.find_element(By.XPATH, value='//*[@id="js-link-box-en"]/small')
             return art_cnt.text
        except Exception as err:
            logging.error(f'Unexpected error: {err}')
        finally:
            self.driver.quit()


def main():
    # keep browser open after code
    i_chrome = ChromeService()

    # a_price = i_chrome.amazon_price()
    # if a_price:
    #     logging.info(f'Retrieved Price: {a_price}')
    # else:
    #     logging.warning('N/A')

    art_cnt = i_chrome.wiki_count()
    if art_cnt:
        logging.info(f'Retrieved Price: {art_cnt}')
    else:
        logging.warning('N/A')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    AMAZON_URL = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'
    WIKI_URL = 'https://www.wikipedia.org/'

    main()