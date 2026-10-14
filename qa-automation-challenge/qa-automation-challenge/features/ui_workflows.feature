Feature: DemoQA browser workflows
  As a QA automation engineer
  I want to exercise the required DemoQA user journeys
  So that the forms, windows, widgets, tables, and interactions are verified

  Scenario: Submit the Practice Form with an uploaded text file
    Given I open the Practice Form from DemoQA
    When I submit a valid Practice Form with an uploaded text file
    Then the submission confirmation popup is open
    When I close the submission popup
    Then the submission popup is closed

  Scenario: Open and close a browser window
    Given I open Browser Windows from DemoQA
    When I open the new browser window
    Then the new window displays the sample page text
    And the new window is closed

  Scenario: Create edit and delete a Web Table record
    Given I open Web Tables from DemoQA
    When I create a Web Table record
    Then the new Web Table record is present
    When I edit the new Web Table record
    Then the edited Web Table record is present
    When I delete the edited Web Table record
    Then the edited Web Table record is absent

  Scenario: Create and delete twelve Web Table records
    Given I open Web Tables from DemoQA
    When I create twelve Web Table records
    Then all twelve new Web Table records are present
    When I delete all twelve new Web Table records
    Then all twelve new Web Table records are absent

  Scenario: Stop and complete the progress bar
    Given I open Progress Bar from DemoQA
    When I stop the progress bar before 25 percent
    Then the progress bar value is at most 25 percent
    When I complete and reset the progress bar
    Then the progress bar is reset to zero

  Scenario: Sort the list items in ascending order
    Given I open Sortable from DemoQA
    When I drag and drop the items into ascending order
    Then the sortable items are in ascending order
