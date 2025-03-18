*** Settings ***

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote
Library    Collections

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown


*** Variables ***

${TITLE}    An edited page
${PAGE_ID}    an-edited-page


*** Test Cases ***

Scenario: As a manager I can add a taxonomy
  Given a logged in manager
    and an page type with a taxonomy
   When I edit the page
    and I select option 'Information Science'
    and I select option 'Information Science » Chronology'
   Then I see '2' selected options

   When I save the page
    and I edit the page
    and I deselect option 'Information Science'
   Then I see '1' selected options

*** Keywords ***

# Given

a logged in manager
    Enable autologin as    Manager

an page type with a taxonomy
    Create content
    ...    type=Document
    ...    title=${TITLE}

    Go to    ${PLONE_URL}/dexterity-types/Document/@@behaviors
    Check Checkbox    //input[@name="form.widgets.collective.taxonomy.generated.test:list"]
    Click    //button[@name="form.buttons.apply"]
    Wait For Condition    Text    //body   contains    Behaviors successfully updated.

# When
I edit the page
    Go to    ${PLONE_URL}/${PAGE_ID}/edit
    Get Text    //body    contains    Edit Page

I select multiple options
    Focus    //select[@name="form.widgets.test.taxonomy_test.from"]
    ${selected} =     Select Options By    //select[@name="form.widgets.test.taxonomy_test.from"]    index    1    2
    Click    //button[@name="from2toButton"]

I save the page
    Click    //button[@name="form.buttons.save"]
    Wait For Condition    Text    //body    contains    Changes saved

I select option '${label}'
    Select Options By    //select[@name="form.widgets.test.taxonomy_test.from"]    label    ${label}
    Click    //button[@name="from2toButton"]

I deselect option '${label}'
    Select Options By    //select[@name="form.widgets.test.taxonomy_test.to"]    label    ${label}
    Click    //button[@name="to2fromButton"]

# Then
I see '${count}' selected options
    Get Element Count    //select[@name="form.widgets.test.taxonomy_test.to"]/option    should be    ${count}

# Misc

Pause
    [Documentation]  Visually pause test execution with interactive dialog by
    ...              importing **Dialogs**-library and calling its
    ...              **Pause Execution**-keyword.
    Import library  Dialogs
    Pause execution

