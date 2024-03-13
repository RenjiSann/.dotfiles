package IntStack is
    function Empty return Boolean;

    procedure Push(n: Integer);
    procedure Pop(n: out Integer) with Pre => Empty;

private
    type IntStack is array(Integer range <>) of Integer;
    stack: IntStack(1..100);
    index: Integer := 1;
end IntStack;