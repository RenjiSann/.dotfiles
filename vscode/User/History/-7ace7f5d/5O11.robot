*** Settings ***
Library    MyClass.py  # Replace with your library/module name

*** Variables ***
${MIN}    42
${MID}    92
${MAX}    142

*** Test Cases ***
Test Initialization With Constructor
    [Tags]    MyClass
    ${obj} =    Evaluate    MyClass.MyClass()

    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Initialization Get Basic
    [Tags]    MyClass
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    ${obj.Get}
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}