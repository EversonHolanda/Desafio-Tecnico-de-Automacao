import pytest
from pytest_bdd import given, scenario, then, when

from qa_automation.api.client import DemoQAApi


@pytest.fixture
def api_context():
    return {"client": DemoQAApi()}


@scenario("../features/api_bookstore.feature", "Create an authorized user and borrow two books")
def test_create_authorized_user_and_borrow_two_books():
    pass


@given("I have a new DemoQA account", target_fixture="api_context")
def create_account(api_context):
    username, password = api_context["client"].new_credentials()
    account = api_context["client"].create_user(username, password)
    api_context.update(username=username, password=password, user_id=account["userID"])
    return api_context


@when("I generate an access token and verify authorization")
def generate_token_and_authorize(api_context):
    token_result = api_context["client"].generate_token(api_context["username"], api_context["password"])
    assert token_result["status"] == "Success"
    api_context["token"] = token_result["token"]
    api_context["authorized"] = api_context["client"].is_authorized(
        api_context["username"], api_context["password"]
    )


@then("the account is authorized")
def account_is_authorized(api_context):
    assert api_context["authorized"] is True


@when("I list available books and borrow two")
def list_and_borrow_books(api_context):
    books = api_context["client"].list_books()
    assert len(books) >= 2, "The catalog must contain at least two books"
    api_context["isbns"] = [book["isbn"] for book in books[:2]]
    api_context["client"].borrow_books(api_context["user_id"], api_context["token"], api_context["isbns"])


@then("the account details include both borrowed books")
def account_has_borrowed_books(api_context):
    user = api_context["client"].get_user(api_context["user_id"], api_context["token"])
    borrowed_isbns = {book["isbn"] for book in user["books"]}
    assert set(api_context["isbns"]).issubset(borrowed_isbns)
