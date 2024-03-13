package IntStack is
    type Stack(Size: Natural) is private;
    type Stack_Access is access Stack;

    -- Return true if the singleton stack is empty.
    function Empty(st: in Stack) return Boolean;

    -- Add a new value at the top of the stack.
    procedure Push(st: in out Stack; n: Integer);

    -- Output the top of the stack if non empty.
    -- Will raise constraint error if the stack is empty.
    procedure Pop(st: in out Stack; n: out Integer) with Pre => not Empty(st);

private
    type StackContent is array(Natural range <>) of Integer;

    type Stack(Size: Natural) is record
        Top: Natural := 1;
        Content: StackContent(1..Size);
    end record;

end IntStack;