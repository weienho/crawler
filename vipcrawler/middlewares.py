# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger


class SeleniumMiddleware:
    def __init__(self, settings=None, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(executable_path=settings.get('WEB_DRIVER_EXECUTABLE_PATH'), service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.settings = settings

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用ChromeDrive抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug('ChromeDrive is Starting')
        try:
            self.browser.get(request.url)
            current_height = 0

            if 'https://www.vip.com/nav' in request.url:
                # 品牌列表处理
                i = 0
                brand_page_roll_times = self.settings.get('BRAND_PAGE_ROLL_TIMES')
                while i < brand_page_roll_times:
                    self.browser.execute_script("window.scrollBy(0, 500)")
                    time.sleep(1)
                    i = i + 1
                    print('')
            elif 'https://list.vip.com/' in request.url:
                page = request.meta.get('page', 1)
                total_page = request.meta.get('total_page', 1)

                if page > 1:
                    if total_page <= 6:
                        self.browser.find_element(By.XPATH,
                                              '//div[@id="J-pagingWrap"]//a[@mars_sead="te_list_main_head_p' + str(
                                                  page) + '"]').click()
                        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'page-select'), str(page)))
                        # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'J-goods-item__img')))
                    else:
                        for i in range(0, page - 1):
                            time.sleep(1)
                            try:
                                self.browser.find_element(By.XPATH,
                                                          '//div[@id="J-pagingWrap"]//a[@id="J_nextPage_link"]').click()
                            except:
                                print('element a id=J_nextPage_link not find')
                                break

                while True:
                    # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    # self.driver.execute_script("var q = document.body.scrollTop = 0")
                    time.sleep(2)
                    self.browser.execute_script("window.scrollBy(0, 500)")

                    check_height = self.browser.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")

                    if check_height == current_height:
                        break

                    current_height = check_height

                # time.sleep(2)
                # self.browser.execute_script("window.scrollBy(0, 500)")
                # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'J-goods-item__img')))
                #  self.browser.find_element_by_css_selector("div#J-pagingWrap > span.page-select + ")
            else:
               self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'main-nav-atag')))
               print(request.url)


            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings,
                   timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
