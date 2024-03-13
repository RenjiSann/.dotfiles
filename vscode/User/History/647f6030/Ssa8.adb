package body IntStack is

    function Empty return Boolean is
    begin
        return index > 0;
    end Empty;

    procedure Push(n: Integer) is
    begin
        stack(index) := n;
        index := index + 1;
    end Push;

    procedure Pop(n: out Integer)
    with
        Pre => Empty
    is
    begin
        index := index - 1;
        n := stack(index);
    end Pop;

end IntStack;