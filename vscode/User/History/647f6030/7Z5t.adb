package body IntStack is
    stack: IntStack(1..100);
    index: Integer := 0;

    procedure Push(n: Integer) is
    begin
        stack(index) := n;
        index := index + 1;
    end Push;

    procedure Pop(n: out Integer)
    with
        Pre => index > 0
    is
    begin
        index := index - 1;
        n := stack(index);
    end Pop;

end IntStack;