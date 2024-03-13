package body IntStack is

    function Empty(st: in Stack) return Boolean is
    begin
        return index = 1;
    end Empty;

    procedure Push(st: in out Stack; n: Integer) is
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