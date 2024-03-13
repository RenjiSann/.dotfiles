package IntStack is
    procedure Push(n: Integer);
    procedure Pop(n: out Integer);

private
    type IntStack is array(100) of Integer;
end IntStack;