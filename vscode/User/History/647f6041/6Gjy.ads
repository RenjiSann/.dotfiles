package IntStack is
    type Stack is private;

    -- Return true if the singleton stack is empty.
    function Empty(st: in Stack) return Boolean;

    -- Add a new value at the top of the stack.
    procedure Push(st: in out Stack; n: Integer);

    -- Output the top of the stack if non empty.
    -- Will raise constraint error if the stack is empty.
    procedure Pop(st: in out Stack; n: out Integer) with Pre => not Empty(st);

private

    subtype IndexType is Natural range 1 .. 512;
    type StackContent is array(IndexType) of Integer;

    type Stack is record
        Top: IndexType := 1;
        Content: StackContent;
    end record;

end IntStack;