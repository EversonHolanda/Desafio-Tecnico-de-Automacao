Feature: DemoQA Book Store API
  As a QA automation engineer
  I want to create and authorize a user and borrow books
  So that the user's final book collection can be verified

  Scenario: Create an authorized user and borrow two books
    Given I have a new DemoQA account
    When I generate an access token and verify authorization
    Then the account is authorized
    When I list available books and borrow two
    Then the account details include both borrowed books
