import secrets
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from qa_automation.pages.base_page import BasePage


class WebTablesPage(BasePage):
    def open(self):
        self.open_section("Elements", "Web Tables")
        page_size = self.visible((By.CSS_SELECTOR, "select.form-control"))
        Select(page_size).select_by_value("20")

    @staticmethod
    def new_record(index=0):
        suffix = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        return {
            "firstName": f"Qa{index}{suffix}",
            "lastName": "Automation",
            "userEmail": f"qa.{suffix}@example.com",
            "age": "32",
            "salary": "65000",
            "department": "Quality Engineering",
        }

    def _row(self, email):
        return self.visible((By.XPATH, f"//tr[td[normalize-space()='{email}']]"))

    def _submit_record(self, record):
        for field_id in ("firstName", "lastName", "userEmail", "age", "salary", "department"):
            field = self.driver.find_element(By.ID, field_id)
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(record[field_id])
        self.click((By.ID, "submit"))

    def create_record(self, record):
        self.click((By.ID, "addNewRecordButton"))
        self._submit_record(record)
        self._row(record["userEmail"])

    def contains_record(self, email):
        return bool(self.driver.find_elements(By.XPATH, f"//tr[td[normalize-space()='{email}']]"))

    def edit_record(self, email, updated_record):
        row = self._row(email)
        self.click((By.XPATH, f"//tr[td[normalize-space()='{email}']]//*[@title='Edit']"))
        self._submit_record(updated_record)
        self._row(updated_record["userEmail"])

    def delete_record(self, email):
        row = self._row(email)
        delete_action = row.find_element(By.CSS_SELECTOR, "[title='Delete']")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", delete_action
        )
        self.wait.until(lambda driver: not self.contains_record(email))
