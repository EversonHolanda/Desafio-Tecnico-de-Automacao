from selenium.webdriver.common.by import By

from qa_automation.pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    def open(self):
        self.open_section("Alerts, Frame & Windows", "Browser Windows")

    def open_new_window(self):
        original = self.driver.current_window_handle
        self.click((By.ID, "windowButton"))
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        new_handle = next(handle for handle in self.driver.window_handles if handle != original)
        self.driver.switch_to.window(new_handle)
        return original

    def sample_page_text(self):
        return self.visible((By.ID, "sampleHeading")).text

    def close_new_window(self, original):
        self.driver.close()
        self.driver.switch_to.window(original)
