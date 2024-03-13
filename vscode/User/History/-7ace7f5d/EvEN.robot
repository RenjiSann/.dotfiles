*** Settings ***
Library    MyClass.py  # Replace with your library/module name

*** Variables ***
${MIN}    42
${MIN_PLUS_ONE}    43
${MID}    92
${MAX}    142
${MAX_LESS_ONE}    141

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
    ${obj.i} =    Convert To Integer    69

    ${c} =    Call Method    ${obj}    Get
    Should Be Equal As Integers    ${c}    69
    Should Be Equal As Integers    ${obj.i}    69

Test Get Max
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Get
    Should Be Equal As Integers    ${c}    ${MAX}
    Should Be Equal As Integers    ${obj.i}    ${MAX}

Test Set Min
    ${obj} =    Evaluate    MyClass.MyClass()
    # ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Set    ${MIN}
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Set Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69

    ${c} =    Call Method    ${obj}    Set    69
    Should Be Equal As Integers    ${c}    69
    Should Be Equal As Integers    ${obj.i}    69

Test Set Max
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Set    ${MAX}
    Should Be Equal As Integers    ${c}    ${MAX}
    Should Be Equal As Integers    ${obj.i}    ${MAX}

Test Set Invalid Below Default
    ${obj} =    Evaluate    MyClass.MyClass()
    ${val} =    Convert To Integer    12

    ${old} =    Convert To Integer    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Below
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69
    ${val} =    Convert To Integer    12

    ${old} =    Convert To Integer    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Over Default
    ${obj} =    Evaluate    MyClass.MyClass()
    ${val} =    Convert To Integer    199

    ${old} =    Convert To Integer    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Set Invalid Over
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69
    ${val} =    Convert To Integer    199

    ${old} =    Convert To Integer    ${obj.i}
    ${c} =    Call Method    ${obj}    Set    ${val}
    Should Be Equal As Integers    ${c}    ${old}
    Should Be Equal As Integers    ${obj.i}    ${old}

Test Incr Default
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    Call Method    ${obj}    Incr
    Should Be Equal As Integers    ${c}    ${MIN_PLUS_ONE}
    Should Be Equal As Integers    ${obj.i}    ${MIN_PLUS_ONE}

Test Incr Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69

    ${old} =    Convert To Integer    ${obj.i}
    ${old_plus_one}=    Evaluate    ${old} + 1
    ${c} =    Call Method    ${obj}    Incr
    Should Be Equal As Integers    ${c}    ${old_plus_one}
    Should Be Equal As Integers    ${obj.i}    ${old_plus_one}

Test Incr Max Value
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Incr
    Should Be Equal As Integers    ${c}    ${MAX}
    Should Be Equal As Integers    ${obj.i}    ${MAX}

Test Decr Default
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    Call Method    ${obj}    Decr
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Decr Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69

    ${old} =    Convert To Integer    ${obj.i}
    ${old_minus_one}=    Evaluate    ${old} - 1
    ${c} =    Call Method    ${obj}    Decr
    Should Be Equal As Integers    ${c}    ${old_minus_one}
    Should Be Equal As Integers    ${obj.i}    ${old_minus_one}

Test Decr Max Value
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Decr
    Should Be Equal As Integers    ${c}    ${MAX_LESS_ONE}
    Should Be Equal As Integers    ${obj.i}    ${MAX_LESS_ONE}

Test Clear Default
    ${obj} =    Evaluate    MyClass.MyClass()

    ${c} =    Call Method    ${obj}    Clear
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Clear Basic
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    69

    ${c} =    Call Method    ${obj}    Clear
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}

Test Clear Max
    ${obj} =    Evaluate    MyClass.MyClass()
    ${obj.i} =    Convert To Integer    ${MAX}

    ${c} =    Call Method    ${obj}    Clear
    Should Be Equal As Integers    ${c}    ${MIN}
    Should Be Equal As Integers    ${obj.i}    ${MIN}