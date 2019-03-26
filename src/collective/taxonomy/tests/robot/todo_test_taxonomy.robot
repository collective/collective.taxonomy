# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.taxonomy -t test_taxonomy.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.solr.testing.COLLECTIVE_SOLR_ROBOT_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/solr/tests/robot/test_search.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  Products/CMFPlone/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  DateTime

Test Setup  TestSetup
Test Teardown  TestTeardown

*** Variables ***

${BROWSER}  chrome


*** Test Cases ***************************************************************

Scenario: As a manager I can add a taxonomy
  Given a loged in manager
   When I search for 'Colorless Green Ideas'
   Then the search returns '1' results
    and the search results should include 'Colorless Green Ideas'

*** Keywords *****************************************************************

# Test Setup/Teardown

TestSetup
  Open test browser
#  a logged in Manager


TestTeardown
#  a logged in Manager
  Close all browsers


# Given

a loged in manager
  Enable autologin as  Manager


# When

I search for '${searchterm}'
  Go to  ${PLONE_URL}/@@search
  Input text  xpath=//main//input[@name='SearchableText']  ${searchterm}

I filter the search by portal type '${portal_type}'
  Click Element  xpath=//button[@id='search-filter-toggle']
  Wait until page contains element  xpath=//input[@id='query-portaltype-Collection']
  Unselect Checkbox  xpath=//input[@id='query-portaltype-Collection']
  Unselect Checkbox  xpath=//input[@id='query-portaltype-Document']

I filter the search by creation date '${date_filter}'
  Click Element  xpath=//button[@id='search-filter-toggle']
  Wait until page contains element  xpath=//input[@id='query-portaltype-Collection']
  Select Radio Button  created  query-date-${date_filter}

# Then

the search returns '${result_count}' results
  Wait until keyword succeeds  5s  1s  XPath Should Match X Times  //strong[@id='search-results-number' and contains(.,'${result_count}')]  1  The search should have returned '${result_count}' results.

the search results should include '${term}'
  Wait until page contains element  xpath=//ol[@class='searchResults']
  Page should contain  ${term}
  XPath Should Match X Times  //div[@id='search-results']//ol//li//a[contains(., '${term}')]  1  Search results should have contained '${term}'.

the search results should not include '${term}'
  Wait until page contains  Search results
  Page should not contain element  xpath=//*[@class='searchResults']/a[contains(text(), '${term}')]


# Misc

Capture screenshot
  [Arguments]  ${filename}
  Capture Page Screenshot  filename=../../../../docs/_screenshots/${filename}
