*** Settings ***
Library    MyClass.py  # Replace with your library/module name

*** Variables ***
${MIN}    42
${MID}    92
${MAX}    142

*** Test Cases ***
Test Initialization With Constructor
    ${obj} =    Evaluate    MyClass.MyClass()

    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Get Default
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    Call Method    ${obj}    Get
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Get Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    69

    ${c} =    Call Method    ${obj}    Get
    Should Be Equal As Integers    ${c}    69
    Should Be Equal As Integers    ${obj.i}    69

Test Get Max
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    ${MAX}

    ${c} =    Call Method    ${obj}    Get
    Should Be Equal As Integers    ${c}    ${MAX}
    Should Be Equal As Integers    ${obj.i}    ${MAX}

Test Set Min
    ${obj} =    Evaluate    MyClass.MyClass()
    # ${obj.i} =    Set Variable    ${MAX}

    ${c} =    Call Method    ${obj}    Set    ${MIN}
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Set Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    69

    ${c} =    Call Method    ${obj}    Set    69
    Should Be Equal As Integers    ${c}    69
    Should Be Equal As Integers    ${obj.i}    69

Test Set Max
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    ${MAX}

    ${c} =    Call Method    ${obj}    Set    ${MAX}
    Should Be Equal As Integers    ${c}    ${MAX}
    Should Be Equal As Integers    ${obj.i}    ${MAX}

Test Set Invalid Below Default
    ${obj} =    Evaluate    MyClass.MyClass()
    ${val} =    Set Variable    12

    ${old} =    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Below
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    69
    ${val} =    Set Variable    12

    ${old} =    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Over Default
    ${obj} =    Evaluate    MyClass.MyClass()
    ${val} =    Set Variable    199

    ${old} =    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Over
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Set Variable    69
    ${val} =    Set Variable    199

    ${old} =    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Incr Default
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    Call Method    ${obj}    Incr
    Should Be Equal As Integers    ${c}    ${MIN} + 1
    Should Be Equal As Integers    ${obj.i}    ${MIN} + 1