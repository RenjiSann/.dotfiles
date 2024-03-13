package IntStack is
    procedure Empty();
    procedure Push(n: Integer);
    procedure Pop(n: out Integer)
    with Pre => index > 0;

private
    type IntStack is array(Integer range <>) of Integer;
    stack: IntStack(1..100);
    index: Integer := 0;
end IntStack;