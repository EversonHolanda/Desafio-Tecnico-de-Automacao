import pytest
from pytest_bdd import given, scenario, then, when

from qa_automation.pages.browser_windows_page import BrowserWindowsPage
from qa_automation.pages.practice_form_page import PracticeFormPage
from qa_automation.pages.progress_bar_page import ProgressBarPage
from qa_automation.pages.sortable_page import SortablePage
from qa_automation.pages.web_tables_page import WebTablesPage


@pytest.fixture
def practice_form(driver):
    return PracticeFormPage(driver)


@pytest.fixture
def browser_windows(driver):
    return BrowserWindowsPage(driver)


@pytest.fixture
def window_context():
    return {}


@pytest.fixture
def web_tables(driver):
    return WebTablesPage(driver)


@pytest.fixture
def table_context():
    return {"emails": []}


@pytest.fixture
def progress_bar(driver):
    return ProgressBarPage(driver)


@pytest.fixture
def sortable(driver):
    return SortablePage(driver)


@scenario("../features/ui_workflows.feature", "Submit the Practice Form with an uploaded text file")
def test_practice_form():
    pass


@scenario("../features/ui_workflows.feature", "Open and close a browser window")
def test_browser_window():
    pass


@scenario("../features/ui_workflows.feature", "Create edit and delete a Web Table record")
def test_web_table_crud():
    pass


@scenario("../features/ui_workflows.feature", "Create and delete twelve Web Table records")
def test_web_table_bulk_records():
    pass


@scenario("../features/ui_workflows.feature", "Stop and complete the progress bar")
def test_progress_bar():
    pass


@scenario("../features/ui_workflows.feature", "Sort the list items in ascending order")
def test_sortable():
    pass


@given("I open the Practice Form from DemoQA")
def open_practice_form(practice_form):
    practice_form.open()


@when("I submit a valid Practice Form with an uploaded text file")
def submit_practice_form(practice_form):
    practice_form.submit_random_form()


@then("the submission confirmation popup is open")
def practice_form_confirmation_open(practice_form):
    assert practice_form.confirmation_is_open()


@when("I close the submission popup")
def close_practice_form_confirmation(practice_form):
    practice_form.close_confirmation()


@then("the submission popup is closed")
def practice_form_confirmation_closed(practice_form):
    practice_form.confirmation_is_closed()


@given("I open Browser Windows from DemoQA")
def open_browser_windows(browser_windows):
    browser_windows.open()


@when("I open the new browser window")
def open_new_browser_window(browser_windows, window_context):
    window_context["original"] = browser_windows.open_new_window()


@then("the new window displays the sample page text")
def sample_page_text_is_validated(browser_windows):
    assert browser_windows.sample_page_text() == "This is a sample page"


@then("the new window is closed")
def new_browser_window_is_closed(browser_windows, window_context):
    browser_windows.close_new_window(window_context["original"])
    assert len(browser_windows.driver.window_handles) == 1


@given("I open Web Tables from DemoQA")
def open_web_tables(web_tables):
    web_tables.open()


@when("I create a Web Table record")
def create_table_record(web_tables, table_context):
    record = web_tables.new_record()
    web_tables.create_record(record)
    table_context["emails"] = [record["userEmail"]]


@then("the new Web Table record is present")
def new_table_record_is_present(web_tables, table_context):
    assert web_tables.contains_record(table_context["emails"][0])


@when("I edit the new Web Table record")
def edit_table_record(web_tables, table_context):
    updated = web_tables.new_record(1)
    web_tables.edit_record(table_context["emails"][0], updated)
    table_context["emails"] = [updated["userEmail"]]


@then("the edited Web Table record is present")
def edited_table_record_is_present(web_tables, table_context):
    assert web_tables.contains_record(table_context["emails"][0])


@when("I delete the edited Web Table record")
def delete_edited_table_record(web_tables, table_context):
    web_tables.delete_record(table_context["emails"][0])


@then("the edited Web Table record is absent")
def edited_table_record_is_absent(web_tables, table_context):
    assert not web_tables.contains_record(table_context["emails"][0])


@when("I create twelve Web Table records")
def create_twelve_table_records(web_tables, table_context):
    records = [web_tables.new_record(index) for index in range(12)]
    for record in records:
        web_tables.create_record(record)
    table_context["emails"] = [record["userEmail"] for record in records]


@then("all twelve new Web Table records are present")
def twelve_table_records_are_present(web_tables, table_context):
    assert all(web_tables.contains_record(email) for email in table_context["emails"])


@when("I delete all twelve new Web Table records")
def delete_twelve_table_records(web_tables, table_context):
    for email in table_context["emails"]:
        if web_tables.contains_record(email):
            web_tables.delete_record(email)


@then("all twelve new Web Table records are absent")
def twelve_table_records_are_absent(web_tables, table_context):
    assert all(not web_tables.contains_record(email) for email in table_context["emails"])


@given("I open Progress Bar from DemoQA")
def open_progress_bar(progress_bar):
    progress_bar.open()


@when("I stop the progress bar before 25 percent")
def stop_progress_bar(progress_bar):
    progress_bar.stop_before_25_percent()


@then("the progress bar value is at most 25 percent")
def progress_bar_is_below_25(progress_bar):
    assert progress_bar.percent() <= 25


@when("I complete and reset the progress bar")
def complete_and_reset_progress_bar(progress_bar):
    progress_bar.complete_and_reset()


@then("the progress bar is reset to zero")
def progress_bar_is_reset(progress_bar):
    assert progress_bar.percent() == 0


@given("I open Sortable from DemoQA")
def open_sortable(sortable):
    sortable.open()


@when("I drag and drop the items into ascending order")
def drag_sortable_items(sortable):
    sortable.sort_ascending()


@then("the sortable items are in ascending order")
def sortable_items_are_ordered(sortable):
    items = [item.text for item in sortable._items()]
    assert items == sorted(sortable.ORDER, key=sortable.ORDER.get)
