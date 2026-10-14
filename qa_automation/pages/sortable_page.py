from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from qa_automation.pages.base_page import BasePage


class SortablePage(BasePage):
    ORDER = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6}

    def open(self):
        self.open_section("Interactions", "Sortable")
        self.wait.until(lambda _driver: self._items())

    def _items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")

    def _drag_to_index(self, text, target_index):
        items = self._items()
        source = next(item for item in items if item.text == text)
        target = items[target_index]
        if source != target:
            ActionChains(self.driver).click_and_hold(source).pause(0.1).move_to_element(target).release().perform()

    def sort_ascending(self):
        current = [item.text for item in self._items()]
        self._drag_to_index(current[-1], 0)
        expected = sorted(self.ORDER, key=self.ORDER.get)
        for target_index, text in enumerate(expected):
            current = [item.text for item in self._items()]
            if current[target_index] != text:
                self._drag_to_index(text, target_index)
        assert [item.text for item in self._items()] == expected
