from selenium.webdriver.common.by import By

from qa_automation.pages.base_page import BasePage


class ProgressBarPage(BasePage):
    def open(self):
        self.open_section("Widgets", "Progress Bar")

    def start(self):
        self.click((By.ID, "startStopButton"))

    def percent(self):
        return int(self.visible((By.CSS_SELECTOR, "#progressBar > div")).get_attribute("aria-valuenow"))

    def stop_before_25_percent(self):
        stopped_at = self.driver.execute_async_script(
            """
            const done = arguments[0];
            const progress = document.querySelector('#progressBar > div');
            const button = document.getElementById('startStopButton');
            let observer;
            let timeout;
            observer = new MutationObserver(() => {
                const percent = Number(progress.getAttribute('aria-valuenow'));
                if (percent >= 15) {
                    observer.disconnect();
                    clearTimeout(timeout);
                    button.click();
                    done(percent);
                }
            });
            observer.observe(progress, {attributes: true, attributeFilter: ['aria-valuenow']});
            timeout = setTimeout(() => {
                observer.disconnect();
                done(Number(progress.getAttribute('aria-valuenow')));
            }, 10000);
            button.click();
            """
        )
        self.wait.until(lambda _driver: self.driver.find_element(By.ID, "startStopButton").text == "Start")
        assert stopped_at <= 25, f"Progress stopped at {stopped_at}%"

    def complete_and_reset(self):
        self.start()
        self.wait.until(lambda _driver: self.percent() == 100)
        self.click((By.ID, "resetButton"))
        self.wait.until(lambda _driver: self.percent() == 0)
