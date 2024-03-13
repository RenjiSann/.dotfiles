package body IntStack is

    function Empty(st: in Stack) return Boolean is
    begin
        return st'Top = 1;
    end Empty;

    procedure Push(st: in out Stack; n: Integer) is
    begin
        st'Content(st'Top) := n;
        st'Top := st'Top + 1;
    end Push;

    procedure Pop(st: in out Stack; n: out Integer) is
    begin
        st'Top := st'Top - 1;
        n := st'Content(st'Top);
    end Pop;

end IntStack;