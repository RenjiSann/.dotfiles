procedure Exo4 is
    subtype RomanNumber is Natural range 1 .. 3999;
    subtype Digit is Natural range 0 .. 9;
    -- (I V X)
    -- (X L C)
    -- (C D M)
    function DigitToString(digit: in Digit; c1: Character; c2: Character; c3: Character) return String is
        ret: String(1 .. 4);
        size: Integer := 0;
    begin
        case digit is
            when 0 => return "";
            when 1 => ret(0) := c1; size := 1;
            when 2 => ret(0) := c1; ret(1) := c1; size := 2;
            when 3 => ret(0) := c1; ret(1) := c1; ret(2) := c1; size := 3;
            when 4 => ret(0) := c1; ret(1) := c2; size := 2;
            when 5 => ret(0) := c2; size := 1;
            when 6 => ret(0) := c2; ret(1) := c1; size := 2;
            when 7 => ret(0) := c2; ret(1) := c1; ret(2) := c1; size := 3;
            when 8 => ret(0) := c2; ret(1) := c1; ret(2) := c1; ret(3) := c1; size := 3;
            when 9 => ret(0) := c1; ret(1) := c3; size := 2;
        end case;

    end DigitToChar;
begin
   null;
end Exo4;