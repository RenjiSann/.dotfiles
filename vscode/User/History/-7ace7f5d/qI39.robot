*** Settings ***
Library    MyClass  # Replace with your library/module name

*** Variables ***
${MIN}    42
${MID}    92
${MAX}    142

*** Test Cases ***
Test Initialization With Constructor
    [Tags]    Class
    ${c} =    MyClass

    Should Be Equal As Integers    ${c.i}    ${MIN}