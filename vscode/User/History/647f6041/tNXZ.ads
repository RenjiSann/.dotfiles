package IntStack is
    procedure Push(n: Integer);
    procedure Pop(n: out Integer);

private
    type IntStack is array(Integer range <>) of Integer;
end IntStack;