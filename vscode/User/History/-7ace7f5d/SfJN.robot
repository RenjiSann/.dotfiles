*** Settings ***
Library    MyClass.py  # Replace with your library/module name

*** Variables ***
${MIN}    42
${MID}    92
${MAX}    142

*** Test Cases ***
Test Initialization With Constructor
    [Tags]    MyClass
    ${c} =    Create Instance    MyClass

    Should Be Equal As Integers    ${c.i}    ${MIN}