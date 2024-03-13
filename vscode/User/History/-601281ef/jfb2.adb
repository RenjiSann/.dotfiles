package body IntStack is
    stack: array (1..512) of Integer;
    index: Integer := 1;

    function Empty return Boolean is
    begin
        return index = 1;
    end Empty;

    procedure Push(n: Integer) is
    begin
        stack(index) := n;
        index := index + 1;
    end Push;

    procedure Pop(n: out Integer) is
    begin
        index := index - 1;
        n := stack(index);
    end Pop;

end IntStack;