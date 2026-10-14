import secrets
import string
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from qa_automation.pages.base_page import BasePage


class PracticeFormPage(BasePage):
    STATE_CITIES = {
        "NCR": ("Delhi", "Gurgaon", "Noida"),
        "Uttar Pradesh": ("Agra", "Lucknow", "Merrut"),
        "Haryana": ("Karnal", "Panipat"),
        "Rajasthan": ("Jaipur", "Jaiselmer", "Kota"),
    }
    SUBJECTS = (
        "Accounting", "Arts", "Biology", "Chemistry", "Commerce", "Computer Science",
        "Civics", "Economics", "English", "Hindi", "History", "Maths", "Physics",
        "Social Studies",
    )
    ADDRESSES = (
        "123 Oak Street, Springfield",
        "45 Market Road, Riverside",
        "780 Central Avenue, Lakewood",
        "16 Garden Lane, Fairview",
    )

    def open(self):
        self.open_section("Forms", "Practice Form")
        self.visible((By.ID, "firstName"))

    def submit_random_form(self):
        first_name = "Qa" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
        last_name = "Test" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(5))
        values = {
            "firstName": first_name,
            "lastName": last_name,
            "userEmail": f"{first_name.lower()}@example.com",
            "userNumber": str(secrets.randbelow(9000000000) + 1000000000),
            "currentAddress": secrets.choice(self.ADDRESSES),
        }
        for field_id, value in values.items():
            self.driver.find_element(By.ID, field_id).send_keys(value)

        self.birth_date = self._random_birth_date()
        self._select_birth_date(self.birth_date)
        gender = secrets.choice(["Male", "Female", "Other"])
        self.click((By.XPATH, f"//label[normalize-space()='{gender}']"))
        hobby = secrets.choice(["Sports", "Reading", "Music"])
        self.click((By.XPATH, f"//label[normalize-space()='{hobby}']"))

        subjects = self.driver.find_element(By.ID, "subjectsInput")
        subject = secrets.choice(self.SUBJECTS)
        subjects.send_keys(subject)
        self._choose_autocomplete_option(subject)
        state = secrets.choice(tuple(self.STATE_CITIES))
        self._select_option("state", state)
        self.wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, "#city input").is_enabled())
        city = secrets.choice(self.STATE_CITIES[state])
        self._select_option("city", city)

        upload = Path(__file__).resolve().parents[2] / "tests" / "data" / "upload.txt"
        self.driver.find_element(By.ID, "uploadPicture").send_keys(str(upload))
        self.click((By.ID, "submit"))

    @staticmethod
    def _random_birth_date():
        today = date.today()
        earliest_year = today.year - 60
        latest_year = today.year - 18
        earliest = date(
            earliest_year,
            today.month,
            min(today.day, monthrange(earliest_year, today.month)[1]),
        )
        latest = date(
            latest_year,
            today.month,
            min(today.day, monthrange(latest_year, today.month)[1]),
        )
        days = (latest - earliest).days
        return earliest + timedelta(days=secrets.randbelow(days + 1))

    def _select_birth_date(self, birth_date):
        self.click((By.ID, "dateOfBirthInput"))
        Select(self.visible((By.CSS_SELECTOR, ".react-datepicker__year-select"))).select_by_value(
            str(birth_date.year)
        )
        Select(self.visible((By.CSS_SELECTOR, ".react-datepicker__month-select"))).select_by_value(
            str(birth_date.month - 1)
        )
        day = self.visible(
            (By.CSS_SELECTOR, f".react-datepicker__day--{birth_date.day:03d}:not(.react-datepicker__day--outside-month)")
        )
        self.driver.execute_script("arguments[0].click();", day)
        expected_value = birth_date.strftime("%d %b %Y").lstrip("0")
        self.wait.until(
            lambda driver: driver.find_element(By.ID, "dateOfBirthInput").get_attribute("value")
            == expected_value
        )

    def _select_option(self, container_id, value):
        container = self.driver.find_element(By.ID, container_id)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", container
        )
        self.visible((By.CSS_SELECTOR, f"#{container_id} input")).send_keys(value)
        self._choose_autocomplete_option(value)

    def _choose_autocomplete_option(self, value):
        option = self.visible((By.XPATH, f"//*[@role='option' and normalize-space()='{value}']"))
        self.driver.execute_script("arguments[0].click();", option)

    def confirmation_is_open(self):
        title = self.visible((By.ID, "example-modal-sizes-title-lg"))
        expected_birth_date = f"{self.birth_date.day} {self.birth_date.strftime('%B')},{self.birth_date.year}"
        return title.is_displayed() and expected_birth_date in self.driver.find_element(
            By.CSS_SELECTOR, ".modal-content"
        ).text

    def close_confirmation(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def confirmation_is_closed(self):
        self.wait.until(EC.invisibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
