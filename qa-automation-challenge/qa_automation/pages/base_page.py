import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = os.getenv("DEMOQA_BASE_URL", "https://demoqa.com").rstrip("/")
        self.wait = WebDriverWait(driver, 15)

    def _ignore_ad_iframes(self):
        self.driver.execute_script(
            "document.querySelectorAll(\"iframe[id*='google_ads_iframe'], iframe[title*='ad content']\")"
            ".forEach(frame => frame.style.setProperty('pointer-events', 'none', 'important'));"
        )

    def open_section(self, section, submenu):
        self.driver.get(self.base_url)
        self._ignore_ad_iframes()
        card = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(concat(' ', normalize-space(@class), ' '), ' card ')][.//h5[normalize-space()='{section}']]",
                )
            )
        )
        title = card.find_element(By.XPATH, ".//h5")
        self.click((By.XPATH, f"//div[contains(concat(' ', normalize-space(@class), ' '), ' card ')][.//h5[normalize-space()='{section}']]//h5"))
        link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{submenu}']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        self._ignore_ad_iframes()
        self.driver.execute_script("arguments[0].click();", link)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._ignore_ad_iframes()
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
