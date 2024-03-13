package IntStack is
    -- Return true if the singleton stack is empty.
    function Empty return Boolean;

    -- Add a new value at the top of the stack.
    procedure Push(n: Integer);

    -- Output the top of the stack if non empty.
    -- Will raise constraint error if the stack is empty.
    procedure Pop(n: out Integer) with Pre => not Empty;

private

    subtype Index is Natural range 1 .. 512;
    type IntStack is array(Index range <>) of Integer;

    stack: IntStack(Index);
    index: Index := 1;
end IntStack;